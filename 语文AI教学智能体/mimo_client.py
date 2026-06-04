"""
MiMo大模型 API 客户端
基于Anthropic格式（Anthropic SDK）
"""
import anthropic
from config import MIMO_API_KEY, MIMO_BASE_URL, MIMO_MODEL, MAX_TOKENS, TEMPERATURE, TOP_P


class MiMoClient:
    """MiMo API 客户端，基于Anthropic SDK"""

    def __init__(self, api_key=None, base_url=None, model=None):
        self.api_key = api_key or MIMO_API_KEY
        self.base_url = base_url or MIMO_BASE_URL
        self.model = model or MIMO_MODEL
        self.client = anthropic.Anthropic(
            api_key=self.api_key,
            base_url=self.base_url
        )

    def chat(self, messages, stream=False, temperature=None, max_tokens=None):
        """
        发送聊天请求
        messages: [{"role": "system/user/assistant", "content": "..."}]
        """
        # 分离 system 消息和其他消息
        system_msg = ""
        chat_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system_msg = msg["content"]
            else:
                chat_messages.append(msg)

        kwargs = {
            "model": self.model,
            "max_tokens": max_tokens or MAX_TOKENS,
            "temperature": temperature or TEMPERATURE,
            "messages": chat_messages,
        }
        if system_msg:
            kwargs["system"] = system_msg

        if stream:
            return self._stream_request(kwargs)
        else:
            return self._normal_request(kwargs)

    def _normal_request(self, kwargs):
        """普通请求"""
        try:
            response = self.client.messages.create(**kwargs)
            return response.content[0].text
        except anthropic.APIConnectionError:
            return "⚠️ 无法连接到MiMo API，请检查服务是否已启动。"
        except anthropic.APIStatusError as e:
            return f"⚠️ API调用出错（{e.status_code}）：{e.message}"
        except Exception as e:
            return f"⚠️ API调用出错：{str(e)}"

    def _stream_request(self, kwargs):
        """流式请求（生成器）"""
        try:
            with self.client.messages.stream(**kwargs) as stream:
                for text in stream.text_stream:
                    yield text
        except anthropic.APIConnectionError:
            yield "\n⚠️ 无法连接到MiMo API，请检查服务是否已启动。"
        except anthropic.APIStatusError as e:
            yield f"\n⚠️ API调用出错（{e.status_code}）：{e.message}"
        except Exception as e:
            yield f"\n⚠️ API调用出错：{str(e)}"

    def test_connection(self):
        """测试API连接"""
        try:
            result = self.chat([
                {"role": "user", "content": "你好，请回复OK"}
            ])
            return True, result
        except Exception as e:
            return False, str(e)


# 全局客户端实例
_client = None


def get_client(**kwargs):
    """获取全局客户端实例"""
    global _client
    if _client is None:
        _client = MiMoClient(**kwargs)
    return _client


def reset_client():
    """重置客户端（更换配置后调用）"""
    global _client
    _client = None
