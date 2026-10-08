# Deploy lên Render + nối Telegram

## 1. Tạo bot Telegram
1. Mở @BotFather → `/newbot` → copy **token**.
2. Lấy Telegram ID của bạn từ @userinfobot (số).

## 2. Đẩy code lên GitHub (repo private)
`acc.txt`, `.env` đã nằm trong `.gitignore` nên mật khẩu guest KHÔNG bị đẩy lên.

## 3. Render
New → **Web Service** → chọn repo → Runtime **Docker** (hoặc New → Blueprint dùng `render.yaml`).
Environment variables:

| Key | Giá trị |
|---|---|
| `TELEGRAM_BOT_TOKEN` | token từ BotFather |
| `ADMIN_IDS` | Telegram ID của bạn (nhiều ID cách nhau dấu phẩy) |
| `ACCOUNTS` | `1=\|UID\|PASSWORD\|VN` (nhiều acc cách nhau dấu `;`) |
| `API_KEY` | (tuỳ chọn) khoá bảo vệ `/5` `/6` → gọi `/5?uid=...&key=API_KEY` |

Không cần đặt `PORT` (Render tự cấp). Health check: `/healthz`.

> Disk của Render là tạm thời: lệnh `/add` ghi vào `acc.txt` sẽ mất khi restart.
> Muốn lưu lâu dài hãy đặt acc trong biến `ACCOUNTS`.
> Bot tự ping `RENDER_EXTERNAL_URL` mỗi 10 phút để free tier không ngủ.

## 4. Kiểm tra
Telegram: `/start`, `/status` (🟢 Online khi đăng nhập game xong), `/5 UID`, `/6 UID`.
Log Render phải có dòng `Telegram connected as @tên_bot`.

## Lỗi thường gặp
- `getUpdates error ... 409`: có 2 nơi cùng chạy bot (máy local + Render) → tắt 1 nơi.
- `Admin only`: chưa đặt `ADMIN_IDS` đúng ID của bạn.
- `Protection Bypass`: Garena chặn account → bot tự dừng thử lại ~6h. Đổi account khác.
