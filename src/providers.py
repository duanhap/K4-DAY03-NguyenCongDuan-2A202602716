"""
🔌 MULTI-PROVIDER LLM ADAPTER (Google Gemini, OpenAI & Offline Mock)
Hỗ trợ Native Tool Calling và chuyển đổi linh hoạt qua biến môi trường LLM_PROVIDER.
"""

import os
import sys
import json
from typing import Dict, Any, List
from dotenv import load_dotenv

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

load_dotenv()

class BaseLLMProvider:
    """Interface cơ sở cho các LLM Provider hỗ trợ Native Tool Calling"""
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        raise NotImplementedError

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        raise NotImplementedError


class MockOfflineProvider(BaseLLMProvider):
    """Offline Mock Provider dùng để chạy thử mà không tốn API Key"""
    def __init__(self):
        self.model_name = "Offline-Mock-Model-2026"

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        return f"[Mock Chatbot Response]: Xin chào! Tôi đã nhận được câu hỏi '{prompt}'. (Chế độ Chatbot không có Tool tra cứu dữ liệu thời gian thực)."

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        prompt_lower = prompt.lower()
        latest_observation = prompt_lower.rsplit("observation from tool '", 1)[-1]
        
        # Mô phỏng quyết định của LLM sau khi nhận Observation từ tool.
        if latest_observation.startswith("send_interview_notification'"):
            return {
                "type": "text",
                "content": "Đã sàng lọc CV đạt yêu cầu và gửi thành công thông báo mời phỏng vấn cho ứng viên.",
                "thought": "Đã hoàn tất quy trình tuyển dụng."
            }
        if latest_observation.startswith("candidate_cv_query'"):
            if '"status": "not_found"' in latest_observation:
                return {
                    "type": "text",
                    "content": "Không tìm thấy hồ sơ ứng viên yêu cầu nên chưa thể đánh giá hoặc gửi thông báo.",
                    "thought": "Ứng viên không tồn tại, không thực hiện thêm hành động."
                }
            if "gửi" in prompt_lower or "thông báo" in prompt_lower:
                return {
                    "type": "tool_call",
                    "tool_name": "send_interview_notification",
                    "arguments": {
                        "candidate_id": "UV2026001",
                        "position": "Kỹ sư Phần mềm Backend",
                        "datetime_str": "14:00 ngày 22/09/2026" if "14:00" in prompt_lower else "09:00 ngày 20/09/2026",
                        "channel": "email"
                    },
                    "thought": "CV đáp ứng tiêu chí tuyển dụng. Tôi sẽ gửi thông báo mời phỏng vấn."
                }
            return {
                "type": "text",
                "content": "CV ứng viên phù hợp với các tiêu chí đã tra cứu.",
                "thought": "Observation đã đủ để trả lời yêu cầu của người dùng."
            }
        if latest_observation.startswith("job_requirements_query'"):
            if "cv" in prompt_lower:
                return {
                    "type": "tool_call",
                    "tool_name": "candidate_cv_query",
                    "arguments": {"candidate_id": "UV2026001"},
                    "thought": "Tiêu chí vị trí đã được tra cứu. Tôi sẽ kiểm tra CV của ứng viên UV2026001."
                }
            return {
                "type": "text",
                "content": "Đã tra cứu tiêu chí tuyển dụng: cấp độ Junior/Mid, yêu cầu Python, REST API, SQL và tối thiểu 1 năm kinh nghiệm.",
                "thought": "Observation đã đủ để trả lời yêu cầu của người dùng."
            }
        if "tra cứu tiêu chí tuyển dụng" in prompt_lower:
            return {
                "type": "tool_call",
                "tool_name": "job_requirements_query",
                "arguments": {"position": "Kỹ sư Phần mềm Backend"},
                "continue_after_tool": True,
                "thought": "Tôi sẽ tra cứu tiêu chí tuyển dụng của vị trí Kỹ sư Phần mềm Backend trước."
            }
        if "tra cứu hồ sơ" in prompt_lower or "tra cứu cv" in prompt_lower:
            candidate_id = "UV9999999" if "uv9999999" in prompt_lower else "UV2026001"
            return {
                "type": "tool_call",
                "tool_name": "candidate_cv_query",
                "arguments": {"candidate_id": candidate_id},
                "thought": f"Tôi sẽ tra cứu CV của ứng viên {candidate_id} bằng tool candidate_cv_query."
            }
        if "gửi thông báo" in prompt_lower or "mời phỏng vấn" in prompt_lower:
            candidate_id = "UV2026001" if "uv2026001" in prompt_lower or "nguyễn văn an" in prompt_lower else "UV9999999"
            datetime_str = "09:00 ngày 20/09/2026" if "09:00" in prompt_lower else "14:00 ngày 22/09/2026"
            return {
                "type": "tool_call",
                "tool_name": "send_interview_notification",
                "arguments": {
                    "candidate_id": candidate_id,
                    "position": "Kỹ sư Phần mềm Backend",
                    "datetime_str": datetime_str,
                    "channel": "email"
                },
                "thought": "Ứng viên đủ điều kiện nhận thông báo mời phỏng vấn. Tôi sẽ gọi tool send_interview_notification."
            }
        if "tiêu chí tuyển dụng" in prompt_lower or "vị trí" in prompt_lower:
            return {
                "type": "tool_call",
                "tool_name": "job_requirements_query",
                "arguments": {"position": "Kỹ sư Phần mềm Backend"},
                "thought": "Tôi sẽ tra cứu tiêu chí tuyển dụng của vị trí Kỹ sư Phần mềm Backend."
            }
        else:
            return {
                "type": "text",
                "content": "[Mock Agent Response]: Quy trình tuyển dụng gồm xác định tiêu chí vị trí, sàng lọc CV theo tiêu chí, phỏng vấn ứng viên phù hợp và gửi thông báo lịch phỏng vấn.",
                "thought": "Câu hỏi chung về tuyển dụng, trả lời trực tiếp không cần gọi Tool."
            }


class GeminiProvider(BaseLLMProvider):
    """Google Gemini Provider (Native Tool Calling với Google GenAI SDK)"""
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model or os.getenv("LLM_MODEL") or "gemini-2.5-flash"

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            return "[Gemini Error]: Chưa cấu hình GEMINI_API_KEY trong file .env! Đang sử dụng chế độ Mock."
        try:
            from google import genai
            client = genai.Client(api_key=self.api_key)
            contents = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            response = client.models.generate_content(model=self.model_name, contents=contents)
            return response.text
        except Exception as e:
            return f"[Gemini Exception]: {str(e)}"

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            print("ℹ️ [Gemini Provider]: Chưa tìm thấy GEMINI_API_KEY hợp lệ. Tự động chuyển sang Mock Offline.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)
        
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=self.api_key)
            
            # Chuẩn hóa function declarations cho Gemini SDK
            function_declarations = []
            for tool in tools_schema:
                # Bỏ qua các tool schema chưa được định nghĩa hoàn chỉnh
                if not tool.get("name") or not tool.get("parameters"):
                    continue
                function_declarations.append({
                    "name": tool["name"],
                    "description": tool.get("description", ""),
                    "parameters": tool.get("parameters", {})
                })

            config = types.GenerateContentConfig(
                system_instruction=system_prompt if system_prompt else None,
                tools=[{"function_declarations": function_declarations}] if function_declarations else None,
                temperature=0.2
            )

            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config
            )

            # Kiểm tra xem Gemini có trả về Tool Call không.
            function_calls = getattr(response, "function_calls", None) or []
            if function_calls:
                call = function_calls[0]
                args = dict(call.args) if hasattr(call, 'args') and call.args else {}
                return {
                    "type": "tool_call",
                    "tool_name": call.name,
                    "arguments": args,
                    "thought": f"Gemini quyết định gọi công cụ '{call.name}' với tham số: {json.dumps(args, ensure_ascii=False)}"
                }
            response_text = getattr(response, "text", None)
            if not response_text:
                text_parts = []
                for candidate in getattr(response, "candidates", None) or []:
                    content = getattr(candidate, "content", None)
                    for part in getattr(content, "parts", None) or []:
                        part_text = getattr(part, "text", None)
                        if part_text:
                            text_parts.append(part_text)
                response_text = "\n".join(text_parts)

            return {
                "type": "text",
                "content": response_text or "Gemini không trả về nội dung văn bản.",
                "thought": "Gemini phản hồi trực tiếp bằng văn bản (không cần gọi công cụ)."
            }

        except Exception as e:
            print(f"⚠️ [Gemini API Warning]: Không thể kết nối live API ({str(e)}). Tự động fallback về Mock.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)


class OpenAIProvider(BaseLLMProvider):
    """OpenAI Provider (Native Tool Calling với OpenAI SDK)"""
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model_name = model or os.getenv("LLM_MODEL") or "gpt-4o-mini"

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            return "[OpenAI Error]: Chưa cấu hình OPENAI_API_KEY trong file .env! Đang sử dụng chế độ Mock."
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            response = client.chat.completions.create(model=self.model_name, messages=messages)
            return response.choices[0].message.content or ""
        except Exception as e:
            return f"[OpenAI Exception]: {str(e)}"

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            print("ℹ️ [OpenAI Provider]: Chưa tìm thấy OPENAI_API_KEY hợp lệ. Tự động chuyển sang Mock Offline.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)

        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)

            tools = []
            for tool in tools_schema:
                if not tool.get("name"):
                    continue
                tools.append({
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool.get("description", ""),
                        "parameters": tool.get("parameters", {})
                    }
                })

            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                tools=tools if tools else None,
                tool_choice="auto" if tools else None
            )

            msg = response.choices[0].message
            if msg.tool_calls:
                call = msg.tool_calls[0]
                args = json.loads(call.function.arguments) if call.function.arguments else {}
                return {
                    "type": "tool_call",
                    "tool_name": call.function.name,
                    "arguments": args,
                    "thought": f"OpenAI quyết định gọi công cụ '{call.function.name}' với tham số: {json.dumps(args, ensure_ascii=False)}"
                }
            else:
                return {
                    "type": "text",
                    "content": msg.content or "",
                    "thought": "OpenAI phản hồi trực tiếp bằng văn bản (không cần gọi công cụ)."
                }
        except Exception as e:
            print(f"⚠️ [OpenAI API Warning]: Không thể kết nối live API ({str(e)}). Tự động fallback về Mock.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)


def get_llm_provider() -> BaseLLMProvider:
    """Factory function khởi tạo Provider theo LLM_PROVIDER env variable"""
    provider_type = os.getenv("LLM_PROVIDER", "gemini").lower()
    
    if provider_type == "gemini":
        key = os.getenv("GEMINI_API_KEY")
        if key and key != "your_gemini_api_key_here":
            return GeminiProvider()
        else:
            return MockOfflineProvider()
    elif provider_type == "openai":
        key = os.getenv("OPENAI_API_KEY")
        if key and key != "your_openai_api_key_here":
            return OpenAIProvider()
        else:
            return MockOfflineProvider()
    elif provider_type == "mock":
        return MockOfflineProvider()
    else:
        return MockOfflineProvider()
