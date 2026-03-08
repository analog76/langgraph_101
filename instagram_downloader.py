import instaloader
import sys
import re
import requests
from pathlib import Path
from urllib.parse import urlparse, parse_qs


def extract_shortcode(value: str) -> str:
    """Accept a full Instagram URL or just the shortcode hash."""
    if value.startswith("http"):
        match = re.search(r"/(?:p|reel)/([A-Za-z0-9_-]+)", value)
        if not match:
            raise ValueError(f"Could not extract shortcode from URL: {value}")
        return match.group(1)
    # Treat plain value as shortcode directly
    return value.strip("/")


def download_all_images(shortcode: str, output_dir: str = ".") -> None:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"Fetching post: {shortcode}")

    loader = instaloader.Instaloader(
        download_videos=False,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        post_metadata_txt_pattern="",
        dirname_pattern=str(output_path),
    )

    post = instaloader.Post.from_shortcode(loader.context, shortcode)

    if post.typename == "GraphSidecar":
        nodes = list(post.get_sidecar_nodes())
        print(f"Carousel post: {len(nodes)} images found")
        for i, node in enumerate(nodes, start=1):
            image_url = node.display_url
            filename = output_path / f"{shortcode}_{i}.jpg"
            print(f"  Downloading {i}/{len(nodes)}: {filename.name}")
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            with open(filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
    else:
        # Single image post
        filename = output_path / f"{shortcode}.jpg"
        print(f"  Downloading single image: {filename.name}")
        response = requests.get(post.url, stream=True)
        response.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

    print(f"\nDone. Saved to: {output_path.resolve()}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python instagram_downloader.py <shortcode_or_url> [output_dir]")
        print("Examples:")
        print("  python instagram_downloader.py DUmseJMkSrI")
        print("  python instagram_downloader.py 'https://www.instagram.com/p/DUmseJMkSrI/?img_index=2'")
        sys.exit(1)

    shortcode = extract_shortcode(sys.argv[1])
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "downloads"

    download_all_images(shortcode, output_dir)
