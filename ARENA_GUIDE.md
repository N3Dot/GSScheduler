# Hướng Dẫn Sử Dụng Hệ Thống Đấu Trường (Arena)

## Tổng quan
Hệ thống đấu trường cho phép người chơi đối đầu với bot được tạo từ dữ liệu của người chơi khác thông qua mã Base64.

## Cách sử dụng

### 1. Vào màn hình Đấu Trường
- Mở ứng dụng và chọn "Đấu Trường" từ menu bên trái

### 2. Load đối thủ
**Cách 1: Sử dụng mã Base64 từ người chơi khác**
- Nhập mã Base64 vào ô "Nhập mã đối thủ"
- Nhấn nút "Load"

**Cách 2: Tạo đối thủ demo**
- Nhấn nút biểu tượng xúc xắc (🎲) để tạo đối thủ demo ngẫu nhiên

### 3. Bắt đầu trận đấu
- Sau khi load đối thủ thành công, nhấn "Bắt Đầu Trận Đấu"
- Trạng thái sẽ hiển thị thông tin của cả hai bên

### 4. Chiến đấu
Chọn một trong 3 loại skill:

**⚔️ Đánh Thường**: 
- Sát thương dựa trên DEX và LUK
- Công thức: 10 + (DEX × 2) + (LUK × 1.5)

**🛡️ Thủ**: 
- Không gây sát thương nhưng giảm 30% + (DEX × 2%) sát thương nhận vào
- Tối đa giảm 80% sát thương

**✨ Phép Thuật**: 
- Sát thương cao dựa trên INT và LUK  
- Công thức: 15 + (INT × 3) + (LUK × 1)

### 5. Kết thúc trận đấu
- Trận đấu kết thúc khi HP của một bên về 0
- Người thắng sẽ nhận được XP và Vàng
- Thưởng = 50 + (Level đối thủ × 10) XP và 25 + (Level đối thủ × 5) Vàng

## Demo Codes có sẵn
Khi khởi động app, hệ thống sẽ tự động tạo 5 mã demo. Copy một trong các mã này để test:

```
Kirito Lv.10: eyJjIjogeyJuIjogIktpcml0byIsICJsIjogMTAsICJoIjogNzIsICJtIjogNjcsICJkIjogMTEsICJpIjogNywgImsiOiA5fX0=

Asuna Lv.8: eyJjIjogeyJuIjogIkFzdW5hIiwgImwiOiA4LCAiaCI6IDk4LCAibSI6IDc2LCAiZCI6IDksICJpIjogMTQsICJrIjogMn19

Natsu Lv.8: eyJjIjogeyJuIjogIk5hdHN1IiwgImwiOiA4LCAiaCI6IDUzLCAibSI6IDYyLCAiZCI6IDExLCAiaSI6IDEzLCAiayI6IDJ9fQ==

Luffy Lv.2: eyJjIjogeyJuIjogIkx1ZmZ5IiwgImwiOiAyLCAiaCI6IDk0LCAibSI6IDkyLCAiZCI6IDEwLCAiaSI6IDYsICJrIjogMTB9fQ==

Goku Lv.10: eyJjIjogeyJuIjogIkdva3UiLCAibCI6IDEwLCAiaCI6IDU5LCAibSI6IDkxLCAiZCI6IDcsICJpIjogMTUsICJrIjogMTJ9fQ==
```

## Tính năng Backend

### Classes chính:
- `Arena`: Quản lý logic đấu trường
- `ArenaBot`: Đại diện cho đối thủ bot
- `SkillType`: Enum định nghĩa các loại skill

### Tính năng nổi bật:
- **Tạo mã Base64**: Mã hóa thông tin nhân vật thành chuỗi Base64 để chia sẻ
- **Giải mã đối thủ**: Parse dữ liệu Base64 thành đối tượng bot
- **AI đơn giản**: Bot chọn skill với tỷ lệ ngẫu nhiên (50% attack, 30% defend, 20% magic)
- **Hệ thống damage**: Công thức damage phức tạp dựa trên stats
- **Battle log**: Ghi lại toàn bộ diễn biến trận đấu

## UI Components
- Battle log với scroll tự động
- Hiển thị thông tin nhân vật realtime  
- Progress bar HP
- Skill buttons với emoji
- Input field cho mã Base64

## Lưu ý
- Mã Base64 có thể được chia sẻ giữa các người chơi
- Hệ thống hỗ trợ cả format dữ liệu rút gọn và đầy đủ
- Bot sẽ mô phỏng hành vi của người chơi thật
- Tất cả tính toán damage đều dựa trên stats thực tế của nhân vật
