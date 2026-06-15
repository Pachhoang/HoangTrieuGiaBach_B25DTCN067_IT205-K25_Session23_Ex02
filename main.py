from storage.disk_manager import calculate_disk_blocks
from storage.io_helper import safe_create_dir
from analytics.time_validator import parse_and_inspect_date


raw_files = [
    {
        "filename": "pod_ep1.mp3",
        "size_bytes": 4500,
        "duration_sec": 180,
        "upload_at": "2026-06-10"
    },
    {
        "filename": "movie_trailer.mp4",
        "size_bytes": 105000,
        "duration_sec": 145,
        "upload_at": "2026-06-31"
    },
    {
        "filename": "clip_short.mp4",
        "size_bytes": 8200,
        "duration_sec": 15,
        "upload_at": "2026-05-15"
    }
]


def get_media_type(filename):
    if filename.lower().endswith(".mp4"):
        return "video"
    return "audio"


def process_files(file_list):
    print("======== HỆ THỐNG QUẢN LÝ LƯU TRỮ RIKKEI MEDIA ======")

    safe_create_dir("media_vault")

    print("[SYSTEM] Kiểm tra hạ tầng lưu trữ... Hoàn tất.")
    print("-" * 75)

    success_count = 0

    for media_file in file_list:
        filename = media_file["filename"]
        size_bytes = media_file["size_bytes"]
        upload_date = media_file["upload_at"]

        print(f"[TỆP TIN: {filename}]")

        parsed_date = parse_and_inspect_date(upload_date)

        if parsed_date is None:
            print(
                f" + Trạng thái phân loại:  THẤT BẠI "
                f"(Lỗi: Định dạng ngày upload '{upload_date}' không tồn tại)"
            )
            print()
            continue

        blocks = calculate_disk_blocks(size_bytes)

        media_type = get_media_type(filename)

        target_dir = f"media_vault/{media_type}"
        safe_create_dir(target_dir)

        print(f" + Dung lượng thực tế: {size_bytes:,} Bytes")
        print(
            f" + Số khối phân vùng (4KB Block): "
            f"{blocks} Blocks"
        )
        print(
            f" + Trạng thái phân loại:  HỢP LỆ "
            f"(Lưu trữ vào thư mục '{media_type}')"
        )
        print()

        success_count += 1

    print("=" * 56)
    print(
        f"TIẾN ĐỘ QUÉT: Hoàn thành xử lý "
        f"{success_count}/{len(file_list)} tệp tin thành công. "
        f"Hệ thống ổn định."
    )


if __name__ == "__main__":
    process_files(raw_files)