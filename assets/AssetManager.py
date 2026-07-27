import base64
from pathlib import Path

class AssetManager:
    """ This class is responsible for handling the conversion of PNGs to base64 text to allow them to be embedded directly in HTML/CSS"""

    def __init__(self, subfolder: str = None, assets_root: Path = None):
        root = assets_root or (Path(__file__).parent / "AssetFiles")
        self.assets_dir = (root / subfolder) if subfolder else root
        self._cache = {} #to not re-read files

    def _png_path(self, name: str) -> Path:
        return self.assets_dir / f"{name}.png"
    def _base64_path(self, name: str) -> Path:
        return self.assets_dir / f"{name}_b64.txt"

    #reads the name.png then b64 encodes it then names it name_b64.txt and returns the encoded string
    def encode(self, name: str) -> str:
        png_path = self._png_path(name)
        if not png_path.exists():
            raise FileNotFoundError(f"No PNG found at {png_path}")

        data = base64.b64encode(png_path.read_bytes()).decode("utf-8")
        self._base64_path(name).write_text(data)
        return data
    #finds every PNG in the assets folder and regenerates its matching b64 text file and returns the list of assets it processed
    def encode_all(self) -> list[str]:
        names = [p.stem for p in self.assets_dir.glob("*.png")]
        for name in names:
            self.encode(name)
        return names

    #returns the b64 string for the given asset name, uses the cache if it was already loaded, otherwise
    #reads the existing b64 txt if available or encodes the png and saves it to be faster
    def get(self, name: str) -> str:
        if name in self._cache:
            return self._cache[name]

        base64_path = self._base64_path(name)
        if base64_path.exists():
            data = base64_path.read_text()
        else:
            data = self.encode(name)

        self._cache[name] = data
        return data

def encode_all_assets(assets_root: Path = None) -> dict:
    root = assets_root or (Path(__file__).parent / "AssetFiles")
    results = {}
    for subfolder in sorted(p for p in root.iterdir() if p.is_dir()):
        manager = AssetManager(subfolder.name, assets_root=root)
        results[subfolder.name] = manager.encode_all()
        return results
