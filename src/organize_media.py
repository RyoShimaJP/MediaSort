import os
from pathlib import Path #フォルダ捜索に使用
from PIL import Image #画像読み取りに使用
from PIL.ExifTags import TAGS #画像読み取りに使用
from datetime import datetime #日付関係に使用
import shutil #ファイル移動に使用

def scan_files(source_folder):
    """
    指定フォルダ内のファイル一覧を再帰的に取得する。

    Parameters:
        source_folder (str or Path): 検索対象のフォルダパス

    Returns:
        List[Path]: メディアファイルのパス一覧（ファイル拡張子などはまだ未フィルタ）
    """

    file_list = []
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            file_path = Path(root) / file
            file_list.append(file_path)
    return file_list

def get_taken_date(filepath):
    """
    画像ファイルからExifの「撮影日(DateTimeOriginal)」を取得する関数
    DateTimeOriginalがないことが多いためDateTimeを使用する

    Parameters:
        filepath (Path): 対象ファイルのパス

    Returns:
        datetime.date or None: 撮影日が取得できればその日付、なければNone
    """
    try:
        img = Image.open(filepath)
        exif_data = img.getexif()

        if exif_data:
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                print(f"Exif Tag: {tag} = {value}")
                if tag == "DateTimeOriginal":
                    # 例: "2022:01:15 12:34:56" → datetime.date に変換
                    return datetime.strptime(value, "%Y:%m:%d %H:%M:%S").date()
                # 撮影日時の代替として DateTime を使用
                if tag == "DateTime":
                    print("DateTimeOriginal が見つからないため、DateTime を代用します。")
                    return datetime.strptime(value, "%Y:%m:%d %H:%M:%S").date()
                
    except Exception as e:
        print(f"[WARNING] Exif取得失敗: {filepath.name} - {e}")
    return None

def get_created_date(filepath):
    """
    ファイルの作成日を取得する関数（Exif取得できなかった場合のフォールバック用）

    Parameters:
        filepath (Path): 対象ファイルのパス

    Returns:
        datetime.date: 作成日（datetime.date型）
    """
    try:
        # Windows：作成日 / Unix：最終更新日
        timestamp = filepath.stat().st_ctime
        return datetime.fromtimestamp(timestamp).date()
    except Exception as e:
        print(f"[WARNING]作成日取得失敗:{filepath.name} - {e}")
        return None

def generate_target_path(filepath: Path, taken_date, created_date, destination_folder: Path) -> Path:
    # 1. 使用する日付を決定
    if taken_date:
        folder_name = taken_date.strftime("%Y-%m-%d")
    elif created_date:
        folder_name = created_date.strftime("%Y-%m-%d")
    else:
        folder_name = "Unknown"

    # 2. 保存先フォルダを定義（destination/YYYY-MM-DD or Unknown）
    target_dir = destination_folder / folder_name
    target_dir.mkdir(parents=True, exist_ok=True)

    # 3. 元のファイル名をそのまま使用
    stem = filepath.stem # 拡張子を除いた部分
    suffix = filepath.suffix # 拡張子（.jpg, .jpegなど）
    new_file_path = target_dir / filepath.name
    counter = 1

    # 4. 重複があれば "_1", "_2", ... を追加して回避
    while new_file_path.exists():
        new_file_path = target_dir / f"{stem}_{counter}{suffix}"
        counter += 1

    return new_file_path

def move_file(source_path: Path, target_path: Path) -> None:
    """
    ファイルを指定された移動先パスに移動する。
    """
    try:
        shutil.move(str(source_path), str(target_path))
        print(f"{source_path.name}を{target_path}に移動しました。")
    except Exception as e:
        print(f"[ERROR] ファイル移動失敗: {source_path.name} - {e}")



def main():
    # フォルダのパス（手動で指定する。後で自動化予定）
    source_folder = Path("test_data") # ←テスト用のフォルダパス
    destination_folder = Path("output")

    print(f"現在の作業ディレクトリ: {Path.cwd()}")
    files = scan_files(source_folder)

    print(f"{len(files)}個のファイルを検出しました:")
    for f in files:
        print(f" - {f.name}")

 #テスト用
        taken_date = get_taken_date(f)
        created_date = get_created_date(f)
        
        print(f"   撮影日: {taken_date}")
        print(f"   作成日: {created_date}")

        target_path = generate_target_path(f, taken_date, created_date, destination_folder)
        print(f"   移動先: {target_path.parent.name}")

        move_file(f, target_path)
    

if __name__ == "__main__":
    main()