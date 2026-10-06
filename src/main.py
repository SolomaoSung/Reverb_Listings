import extract
import transform
import data_quality
import load

def main()-> int:
    raw_path = extract.run()

    processed_path = transform.run(raw_path)

    if data_quality.run(processed_path) == 1:
        return 1
    
    load.run(processed_path)
    
    return 0

if __name__ == "__main__":
    raise SystemExit(main())