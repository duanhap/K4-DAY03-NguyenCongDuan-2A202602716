"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
"""

import json
from typing import Dict, Any

# ============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA
# ============================================================================

TOOLS_SCHEMA = [
    {
        "name": "job_requirements_query",
        "description": "Tra cứu tiêu chí tuyển dụng của một vị trí.",
        "parameters": {
            "type": "object",
            "properties": {
                "position": {
                    "type": "string",
                    "description": "Tên vị trí cần tra cứu, ví dụ: 'Kỹ sư Phần mềm Backend'"
                }
            },
            "required": ["position"]
        }
    },
    {
        "name": "candidate_cv_query",
        "description": "Tra cứu hồ sơ và nội dung CV của ứng viên.",
        "parameters": {
            "type": "object",
            "properties": {
                "candidate_id": {
                    "type": "string",
                    "description": "Mã ứng viên, ví dụ: 'UV2026001'"
                }
            },
            "required": ["candidate_id"]
        }
    },
    {
        "name": "send_interview_notification",
        "description": "Gửi thông báo mời ứng viên tham dự phỏng vấn.",
        "parameters": {
            "type": "object",
            "properties": {
                "candidate_id": {
                    "type": "string",
                    "description": "Mã ứng viên nhận thông báo"
                },
                "position": {
                    "type": "string",
                    "description": "Vị trí tuyển dụng"
                },
                "datetime_str": {
                    "type": "string",
                    "description": "Thời gian phỏng vấn, ví dụ: '09:00 ngày 20/09/2026'"
                },
                "channel": {
                    "type": "string",
                    "description": "Kênh gửi thông báo, ví dụ: 'email'"
                }
            },
            "required": ["candidate_id", "position", "datetime_str", "channel"]
        }
    }
]

# ============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ============================================================================

JOB_REQUIREMENTS = {
    "Kỹ sư Phần mềm Backend": {
        "level": "Junior/Mid",
        "skills": ["Python", "REST API", "SQL"],
        "experience_years": 1,
        "education": "Công nghệ thông tin hoặc ngành liên quan"
    }
}

CANDIDATE_DATABASE = {
    "UV2026001": {
        "full_name": "Nguyễn Văn An",
        "email": "an.nguyen@example.com",
        "skills": ["Python", "REST API", "SQL"],
        "experience_years": 2,
        "education": "Công nghệ thông tin"
    }
}


def execute_job_requirements_query(position: str) -> str:
    """Tra cứu tiêu chí tuyển dụng theo vị trí."""
    requirements = JOB_REQUIREMENTS.get(position.strip())
    if requirements:
        return json.dumps({
            "status": "SUCCESS",
            "position": position,
            "data": requirements
        }, ensure_ascii=False)
    return json.dumps({
        "status": "NOT_FOUND",
        "message": f"Chưa có tiêu chí tuyển dụng cho vị trí '{position}'."
    }, ensure_ascii=False)


def execute_candidate_cv_query(candidate_id: str) -> str:
    """Tra cứu hồ sơ và CV của ứng viên."""
    candidate = CANDIDATE_DATABASE.get(candidate_id.strip().upper())
    if candidate:
        return json.dumps({
            "status": "SUCCESS",
            "candidate_id": candidate_id,
            "data": candidate
        }, ensure_ascii=False)
    return json.dumps({
        "status": "NOT_FOUND",
        "message": f"Không tìm thấy hồ sơ ứng viên có mã '{candidate_id}'."
    }, ensure_ascii=False)


def execute_send_interview_notification(candidate_id: str, position: str, datetime_str: str, channel: str) -> str:
    """Gửi thông báo mời phỏng vấn cho ứng viên."""
    candidate = CANDIDATE_DATABASE.get(candidate_id.strip().upper())
    if not candidate:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không thể gửi thông báo vì không tìm thấy ứng viên '{candidate_id}'."
        }, ensure_ascii=False)
    return json.dumps({
        "status": "SUCCESS",
        "notification_id": f"NT-{candidate_id}-99",
        "candidate_id": candidate_id,
        "recipient": candidate["email"],
        "position": position,
        "datetime": datetime_str,
        "channel": channel,
        "message": f"Đã gửi thông báo mời phỏng vấn vị trí {position} cho {candidate['full_name']} vào {datetime_str} qua {channel}."
    }, ensure_ascii=False)


# Router gọi tool thực tế
TOOL_ROUTER = {
    "job_requirements_query": execute_job_requirements_query,
    "candidate_cv_query": execute_candidate_cv_query,
    "send_interview_notification": execute_send_interview_notification
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)
