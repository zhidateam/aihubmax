"""
AIHubMax 临时文件服务模块
提供临时文件上传功能
"""
import os
from typing import Dict, Union, BinaryIO
from pathlib import Path

from ..client import AIHubMaxClient
from ..const import AIHUBMAX_API_HOST

# 临时文件上传URI
TMPFILE_UPLOAD_URI = "/ability/tmpfile/upload"

async def upload_file(client: AIHubMaxClient, file_path: Union[str, Path, BinaryIO], file_name: str = None) -> Dict:
    """
    上传文件到临时文件服务

    Args:
        client: AIHubMaxClient实例
        file_path: 文件路径或文件对象
        file_name: 文件名（如果file_path是文件对象，则必须提供）

    Returns:
        上传结果，包含访问URL
        {
            "url": "https://tmpfile.zooai.cc/uploads/2023/04/10/abc123.jpg",
            "quota": 1
        }
    """
    url = f"{AIHUBMAX_API_HOST}{TMPFILE_UPLOAD_URI}"

    # 处理不同类型的文件输入
    if isinstance(file_path, (str, Path)):
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")

        if not file_name:
            file_name = file_path.name

        with open(file_path, "rb") as f:
            files = {"file": (file_name, f.read())}
            response = await client._request("POST", url, files=files)
    else:
        # 文件对象
        if not file_name:
            raise ValueError("使用文件对象时必须提供file_name参数")

        files = {"file": (file_name, file_path)}
        response = await client._request("POST", url, files=files)

    return response.get("data", {})
