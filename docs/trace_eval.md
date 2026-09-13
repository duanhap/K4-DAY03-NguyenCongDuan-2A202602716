# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Nguyễn Công Duẩn 
> **Mã Sinh Viên / Mã Học viên:** 2A202602716  
> **Chủ đề Lựa chọn:** *Trợ lý Tuyển dụng & Sàng lọc CV:* Tra cứu tiêu chí tuyển dụng vị trí và gửi thông báo lịch phỏng vấn.

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | **4 / 5** | Trợ lý phải phân tích yêu cầu tuyển dụng, tra cứu tiêu chí của vị trí, đọc và đối chiếu thông tin trong CV, đánh giá mức độ phù hợp, rồi mới đề xuất hoặc gửi lịch phỏng vấn. Đây chính là chuỗi suy luận nhiều bước. |
| **2. Tool Interaction** | **3 / 5** | Hệ thống cần gọi các công cụ qua MCP Server để tra cứu tiêu chí tuyển dụng, lấy dữ liệu CV/ứng viên, kiểm tra lịch trống và gửi thông báo hoặc lời mời phỏng vấn. Các thao tác này cần kết nối với dữ liệu và dịch vụ bên ngoài thay vì chỉ sinh văn bản. |
| **3. Dynamic Decision** | **4 / 5** | Quyết định của Agent có phụ thuộc vào Observation từ từng tool: nếu CV đạt tiêu chí thì chuyển sang kiểm tra lịch và đặt lịch; nếu thiếu điều kiện thì yêu cầu bổ sung hoặc từ chối; nếu không tìm thấy dữ liệu thì báo lỗi và không được tự bịa thông tin. |
| **4. Long Horizon Goal** | **4 / 5** | Agent theo đuổi mục tiêu xuyên suốt từ lúc tiếp nhận nhu cầu tuyển dụng đến khi hoàn tất sàng lọc và thông báo lịch phỏng vấn, có thể qua nhiều lượt xử lý.|
| **TỔNG ĐIỂM AGENTIC FIT** | **15 / 20** | *Tổng điểm 15/20, cao hơn 12/20: bài toán rất phù hợp để triển khai Agentic System vì có nhiều bước suy luận, tương tác tool và quyết định dựa trên dữ liệu quan sát.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

```json
[
{
    "step": 1,
    "query": "Hãy tra cứu tiêu chí tuyển dụng vị trí Kỹ sư Phần mềm Backend, kiểm tra mức độ phù hợp của CV ứng viên UV2026001, rồi nếu đạt yêu cầu hãy gửi thông báo mời phỏng vấn vào lúc 14:00 ngày 22/09/2026 qua email.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "job_requirements_query",
    "arguments": {
      "position": "Kỹ sư Phần mềm Backend"
    },
    "observation": {
      "status": "SUCCESS",
      "position": "Kỹ sư Phần mềm Backend",
      "data": {
        "level": "Junior/Mid",
        "skills": [
          "Python",
          "REST API",
          "SQL"
        ],
        "experience_years": 1,
        "education": "Công nghệ thông tin hoặc ngành liên quan"
      }
    },
    "latency_ms": 1124.69
  },
  {
    "step": 2,
    "query": "Hãy tra cứu tiêu chí tuyển dụng vị trí Kỹ sư Phần mềm Backend, kiểm tra mức độ phù hợp của CV ứng viên UV2026001, rồi nếu đạt yêu cầu hãy gửi thông báo mời phỏng vấn vào lúc 14:00 ngày 22/09/2026 qua email.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "candidate_cv_query",
    "arguments": {
      "candidate_id": "UV2026001"
    },
    "observation": {
      "status": "SUCCESS",
      "candidate_id": "UV2026001",
      "data": {
        "full_name": "Nguyễn Văn An",
        "email": "an.nguyen@example.com",
        "skills": [
          "Python",
          "REST API",
          "SQL"
        ],
        "experience_years": 2,
        "education": "Công nghệ thông tin"
      }
    },
    "latency_ms": 1035.0
  },
  {
    "step": 3,
    "query": "Hãy tra cứu tiêu chí tuyển dụng vị trí Kỹ sư Phần mềm Backend, kiểm tra mức độ phù hợp của CV ứng viên UV2026001, rồi nếu đạt yêu cầu hãy gửi thông báo mời phỏng vấn vào lúc 14:00 ngày 22/09/2026 qua email.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "send_interview_notification",
    "arguments": {
      "channel": "email",
      "datetime_str": "14:00 ngày 22/09/2026",
      "candidate_id": "UV2026001",
      "position": "Kỹ sư Phần mềm Backend"
    },
    "observation": {
      "status": "SUCCESS",
      "notification_id": "NT-UV2026001-99",
      "candidate_id": "UV2026001",
      "recipient": "an.nguyen@example.com",
      "position": "Kỹ sư Phần mềm Backend",
      "datetime": "14:00 ngày 22/09/2026",
      "channel": "email",
      "message": "Đã gửi thông báo mời phỏng vấn vị trí Kỹ sư Phần mềm Backend cho Nguyễn Văn An vào 14:00 ngày 22/09/2026 qua email."
    },
    "latency_ms": 1343.75
  },
  {
    "step": 4,
    "query": "Hãy tra cứu tiêu chí tuyển dụng vị trí Kỹ sư Phần mềm Backend, kiểm tra mức độ phù hợp của CV ứng viên UV2026001, rồi nếu đạt yêu cầu hãy gửi thông báo mời phỏng vấn vào lúc 14:00 ngày 22/09/2026 qua email.",
    "action_type": "FINAL_ANSWER",
    "thought": "Gemini phản hồi trực tiếp bằng văn bản (không cần gọi công cụ).",
    "output": "Dựa trên các bước đã thực hiện, đây là kết quả chi tiết:\n\n1. **Tiêu chí tuyển dụng vị trí Kỹ sư Phần mềm Backend:**\n   - **Cấp độ:** Junior/Mid\n   - **Kỹ năng yêu cầu:** Python, REST API, SQL\n   - **Kinh nghiệm:** Từ 1 năm trở lên\n   - **Học vấn:** Tốt nghiệp chuyên ngành Công nghệ thông tin hoặc ngành liên quan.\n\n2. **Kiểm tra mức độ phù hợp của ứng viên UV2026001 (Nguyễn Văn An):**\n   - **Kỹ năng:** Có đầy đủ các kỹ năng yêu cầu (Python, REST API, SQL).\n   - **Kinh nghiệm:** 2 năm kinh nghiệm (đạt yêu cầu tối thiểu 1 năm).\n   - **Học vấn:** Tốt nghiệp Công nghệ thông tin (đạt yêu cầu).\n   - *Kết luận:* Ứng viên đạt yêu cầu tuyển dụng.\n\n3. **Thông báo phỏng vấn:**\n   - Đã gửi thành công thông báo mời phỏng vấn qua **email** (đến địa chỉ: an.nguyen@example.com) cho ứng viên Nguyễn Văn An vào lúc **14:00 ngày 22/09/2026** cho vị trí Kỹ sư Phần mềm Backend (Mã thông báo: `NT-UV2026001-99`).",
    "latency_ms": 2002.57
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [x] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Gemini/OpenAI).
- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 6 / 6 lượt (TC02: 1, TC03: 1, TC04: 3, TC05: 1).
- **Kết quả đẩy Repo nộp bài:** [x] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
