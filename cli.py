
import sys

from textcleaner.pipeline import CleaningPipeline
def main():
    if len(sys.argv) < 2:
        print("Usage: python cli.py <path_to_file.xlsx>")
        sys.exit(1)

    path = sys.argv[1]
    pipeline = CleaningPipeline(path)
    pipeline.preview_columns()

    text_input = input("\nText columns to clean (comma-separated): ")
    text_columns = [c.strip() for c in text_input.split(",") if c.strip()]

    drop_input = input("Columns to drop (comma-separated, leave empty if none): ")
    drop_columns = [c.strip() for c in drop_input.split(",") if c.strip()]

    output_path = input("Output file name [cleaned.xlsx]: ").strip() or "cleaned.xlsx"

    pipeline.run(
        text_columns=text_columns,
        drop_columns=drop_columns,
        output_path=output_path,
    )


if __name__ == "__main__":
    main()
