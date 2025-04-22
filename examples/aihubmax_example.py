"""
AIHubMax API使用示例
"""
import os
import asyncio
from aihubmax import AIHubMaxClient, tmpfile

# 设置环境变量（也可以直接在代码中传入token）
# os.environ["AIHUBMAX_TOKEN"] = "your_token_here"

async def upload_file_example(token: str):
    """上传文件示例"""
    async with AIHubMaxClient(token=token) as client:
        try:
            # 创建一个测试文件
            test_file_path = "examples/test_file.txt"
            with open(test_file_path, "w") as f:
                f.write("This is a test file for AIHubMax API")

            # 上传文件
            result = await tmpfile.upload_file(client, test_file_path)
            print(f"文件上传成功，URL: {result.get('url')}")
            print(f"使用配额: {result.get('quota')}")

            # 也可以使用文件对象
            with open(test_file_path, "rb") as f:
                result = await tmpfile.upload_file(client, f, file_name="test_file_from_object.txt")
                print(f"文件对象上传成功，URL: {result.get('url')}")

            return result
        except Exception as e:
            print(f"文件上传失败: {e}")
            return None
        finally:
            # 清理测试文件
            if os.path.exists(test_file_path):
                os.remove(test_file_path)

async def main():
    """主函数"""
    print("开始AIHubMax API示例")

    # 设置token
    token = "sk-"  # 替换为你的token

    # 上传文件
    result = await upload_file_example(token)

    if result:
        print("测试完成")
    else:
        print("测试失败")

if __name__ == "__main__":
    asyncio.run(main())
