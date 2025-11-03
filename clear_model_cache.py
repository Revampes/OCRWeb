"""
Clear HuggingFace model cache for DeepSeek-OCR
Run this if you're having persistent import errors with the model
"""
import os
import shutil
from pathlib import Path

def clear_deepseek_cache():
    """Clear the DeepSeek-OCR model cache"""
    
    # Common cache locations
    cache_paths = [
        Path.home() / ".cache" / "huggingface" / "hub",
        Path.home() / ".cache" / "huggingface" / "modules",
    ]
    
    print("=" * 60)
    print("DeepSeek-OCR Cache Cleaner")
    print("=" * 60)
    
    found_items = []
    
    for cache_path in cache_paths:
        if cache_path.exists():
            print(f"\n📂 Checking: {cache_path}")
            
            # Look for DeepSeek-OCR related items
            for item in cache_path.iterdir():
                if 'deepseek' in item.name.lower() or 'ocr' in item.name.lower():
                    found_items.append(item)
                    print(f"   Found: {item.name}")
    
    if not found_items:
        print("\n✓ No DeepSeek-OCR cache found. Nothing to clear.")
        print("  This might mean the model hasn't been downloaded yet.")
        return
    
    print(f"\n⚠️  Found {len(found_items)} cache item(s)")
    print("\nThis will DELETE the cached model files.")
    print("The model will be re-downloaded on next use (~8GB).")
    
    response = input("\nContinue? (yes/no): ").strip().lower()
    
    if response in ['yes', 'y']:
        print("\n🗑️  Clearing cache...")
        
        for item in found_items:
            try:
                if item.is_file():
                    item.unlink()
                    print(f"   ✓ Deleted file: {item.name}")
                elif item.is_dir():
                    shutil.rmtree(item)
                    print(f"   ✓ Deleted directory: {item.name}")
            except Exception as e:
                print(f"   ✗ Error deleting {item.name}: {e}")
        
        print("\n✅ Cache cleared successfully!")
        print("\n💡 Next steps:")
        print("   1. Restart your Flask server")
        print("   2. The model will download fresh on first OCR request")
        print("   3. This should fix any cached code issues")
        
    else:
        print("\n❌ Cache clearing cancelled.")

if __name__ == "__main__":
    try:
        clear_deepseek_cache()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
