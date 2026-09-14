# AppOps: bản chốt kiến trúc

## Mình đang xây gì?

AppOps là nền tảng hỗ trợ và vận hành phần mềm. Ban đầu người dùng hỏi cách thao tác, hệ thống trả lời theo tài liệu được duyệt và đính kèm đúng ảnh. Về sau AppOps nhận ticket Jira, phân loại, giao việc cho đúng vai trò, đọc dữ liệu chẩn đoán được phép, nhắc phản hồi, xin phê duyệt và thực hiện một số thao tác vận hành có kiểm soát.

Khoảng 15 phần mềm là 15 phạm vi quản lý trong một nền tảng, không phải 15 bản chatbot riêng. Người dùng chọn phần mềm và môi trường; quyền truy cập phải được kiểm tra trước khi tìm tài liệu hoặc thực hiện hành động.

## Công nghệ đã chọn

| Thành phần | Chọn gì | Vai trò |
| --- | --- | --- |
| Giao diện | Next.js, React, TypeScript | Màn hình người dùng và bàn làm việc vận hành |
| Xử lý nghiệp vụ | Python, FastAPI | API và các quy tắc nghiệp vụ |
| Lưu dữ liệu | PostgreSQL và pgvector | Hồ sơ, quyền, tài liệu đã tách, tìm kiếm theo nghĩa |
| Quy trình dài ngày | Temporal | Giữ việc đang chờ, hẹn giờ và tiếp tục sau khi tiến trình khởi động lại |
| Đọc tài liệu | pdfplumber, pypdfium2, python-docx | Lấy chữ, cấu trúc, vị trí ảnh và ảnh chụp từ nguồn |
| Tìm kiếm bằng AI | Qwen3-Embedding-0.6B chạy nội bộ | Chuyển câu hỏi/đoạn tài liệu thành biểu diễn số để tìm phần gần nghĩa |
| Soạn câu trả lời | Hồ sơ model qua OpenRouter | Đọc phần tài liệu đã tìm và soạn trả lời; phải kiểm chứng trước khi bật |
| Đăng nhập | Keycloak qua OpenID Connect | Xác minh tài khoản; AppOps kiểm tra quyền theo từng ứng dụng |
| Lưu file | R2 riêng tư khi triển khai | Giữ PDF, ảnh, bằng chứng; không công khai file |
| Theo dõi | OpenTelemetry và bộ Grafana | Xem lỗi, độ trễ, dấu vết xử lý và tình trạng hệ thống |
| Triển khai | Docker Compose trên máy chủ Ubuntu | Cấu hình triển khai có thể lặp lại và sao lưu/phục hồi |

Không đưa Kafka, Kubernetes, Qdrant, nhiều framework agent hoặc kho dữ liệu phân tích vào bản đầu. Chỉ bổ sung khi có giới hạn thực tế đã đo được.

## Ba điểm phải giữ

**Tài liệu không tự biến thành quyền thao tác.** Một hướng dẫn ghi người dùng bấm nút nào không có nghĩa AI được quyền bấm thay. Quy trình phải ghi vai trò, điều kiện, mức rủi ro và cách kiểm tra kết quả. Thao tác tự động còn cần một chức năng tích hợp đã đăng ký và được cho phép.

**Ticket phải có người và quy tắc chịu trách nhiệm.** Jira giữ trạng thái ticket chính thức. AppOps theo dõi phần việc nội bộ và lịch nhắc. Đóng vì không phản hồi phải được ghi đúng lý do, không được tính thành đã sửa xong lỗi kỹ thuật. Ban đầu tự động gửi/đóng đều tắt cho đến khi được duyệt.

**Truy vết phải giải thích được việc đã xảy ra.** Từ ticket phải lần ra được nguồn hướng dẫn, bằng chứng, câu trả lời, ai duyệt, thao tác nào được thực hiện, kết quả kiểm tra và lý do đóng. Không chỉ ghi một dòng 'AI đã xử lý'.

## Cấu trúc code

Chọn modular monolith, nghĩa là một ứng dụng chính được chia module rõ trách nhiệm. Giao diện, API và tiến trình xử lý nền chạy riêng khi cần, nhưng không tách thành quá nhiều dịch vụ nhỏ ngay từ đầu.

Các module gồm danh tính, danh mục ứng dụng, chính sách quyền, kiến thức, hội thoại, hồ sơ hỗ trợ, điều phối tự động, tích hợp, bằng chứng và nhật ký kiểm toán. Code lõi nghiệp vụ không phụ thuộc trực tiếp thư viện web, cơ sở dữ liệu hay nhà cung cấp AI. Nhờ vậy thay connector hoặc model không phải sửa mọi nơi.

## Tiến độ đúng nghĩa

Bộ tài liệu hiện tại là thiết kế và quy tắc phát triển, chưa phải phần mềm chạy được. Thứ tự xây: S0 nền ứng dụng và đăng nhập; S1 lõi hồ sơ/quy trình; S2 tài liệu và hỏi đáp có ảnh; S3 Jira; S4 Telegram/Zalo; S5 chẩn đoán chỉ đọc; S6 thao tác được duyệt.

Mỗi bước có tiêu chí nghiệm thu và bằng chứng kiểm tra. Ông review giao diện, luồng sử dụng và chính sách vận hành. Kiểm thử và review kỹ thuật phải được thực hiện riêng, không đẩy trách nhiệm đọc code sang ông.

## Thuật ngữ

**RAG:** tìm tài liệu liên quan rồi đưa cho model đọc để trả lời. **Embedding:** biểu diễn số giúp tìm theo nghĩa. **Adapter:** lớp chuyển đổi để kết nối một hệ thống cụ thể. **Workflow:** quy trình có trạng thái và các bước xử lý. **Idempotency:** nhận lại cùng yêu cầu nhưng không tạo thêm tác dụng ngoài ý muốn. **Reconciliation:** đối chiếu lại với hệ thống nguồn khi thông tin lệch hoặc kết quả chưa rõ. **Audit:** nhật ký ai làm gì, theo quyền nào và kết quả gì. **RPO:** mức mất dữ liệu tối đa đặt mục tiêu. **RTO:** thời gian đặt mục tiêu để phục hồi. Các mục tiêu phục hồi phải được diễn tập, không phải ghi vào tài liệu là đã đạt.

Đọc tiếp tại [mục lục](../README.md) và [trạng thái](../status.md).
