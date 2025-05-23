"""
AIHubMax API异步客户端
"""
import os
import json
import httpx
import traceback
from typing import Dict, List, Optional, Any

from loguru import logger
from .const import *
from .exception import AIHubMaxException


class AIHubMaxClient:
    """
    AIHubMax API异步客户端
    提供对AIHubMax API的异步访问
    """
    def __init__(self, token: str = os.getenv("AIHUBMAX_TOKEN"), timeout: float = 30.0, print_log: bool = True):
        """
        初始化AIHubMax API客户端

        Args:
            token: AIHubMax API令牌
            timeout: API请求超时时间（秒）
            print_log: 是否打印API请求日志
        """
        if not token:
            raise ValueError("AIHubMax API令牌不能为空，请提供token参数或设置AIHUBMAX_TOKEN环境变量")

        self._token = token
        self.print_log = print_log
        self.client = httpx.AsyncClient(timeout=timeout)

    async def close(self) -> None:
        """
        关闭异步客户端
        """
        if self.client:
            await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def _request(self, method: str, url: str, data: Dict = None, files: Dict = None, check_code: bool = True) -> Dict:
        """
        发送API请求

        Args:
            method: HTTP方法（GET, POST, PUT, DELETE）
            url: API URL
            data: 请求数据
            files: 文件数据
            check_code: 是否检查响应代码

        Returns:
            API响应数据
        """
        headers = {
            "Authorization": f"Bearer {self._token}"
        }

        if not files:
            headers["Content-Type"] = "application/json"

        if self.print_log:
            logger.debug(f"{method} 请求AIHubMax接口: {url}")
            if data and not files:
                logger.debug(f"请求体: {data}")
            elif files:
                logger.debug(f"上传文件: {list(files.keys())}")

        try:
            if method.upper() == "GET":
                response = await self.client.get(url, headers=headers)
            elif method.upper() == "POST" and files:
                logger.debug(f"上传文件到 {url}，headers: {headers}")
                response = await self.client.post(url, headers=headers, files=files)
            else:
                response = await self.client.request(
                    method.upper(),
                    url,
                    headers=headers,
                    json=data
                )

            response.raise_for_status()
            resp_data = response.json()

            if self.print_log:
                logger.debug(f"AIHubMax接口响应: {resp_data}")

            if check_code and resp_data.get("code", -1) != 0:
                logger.error(f"接口返回错误, URL: {url}, 错误信息: {resp_data}")
                raise AIHubMaxException(
                    code=resp_data.get("code"),
                    msg=resp_data.get("msg"),
                    url=url,
                    req_body=data,
                    headers=headers
                )

            return resp_data
        except httpx.HTTPError as e:
            logger.error(f"请求AIHubMax接口异常: {e}, URL: {url}")
            logger.error(f"异常详情: {traceback.format_exc()}")
            raise AIHubMaxException(
                code=-1,
                msg=f"请求失败: {str(e)}",
                url=url,
                req_body=data,
                headers=headers
            )
        except json.JSONDecodeError as e:
            logger.error(f"解析响应JSON失败: {e}, URL: {url}")
            raise AIHubMaxException(
                code=-1,
                msg="响应解析失败",
                url=url,
                req_body=data,
                headers=headers
            )
        except Exception as e:
            tb = traceback.format_exc()
            logger.error(f"请求AIHubMax接口未知异常: {e}, URL: {url}\n{tb}")
            raise AIHubMaxException(
                code=-1,
                msg=f"未知错误: {str(e)}",
                url=url,
                req_body=data,
                headers=headers
            )


