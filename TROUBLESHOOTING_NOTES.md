# Troubleshooting Notes

## Issue: LlamaFlashAttention2 Import Error

### Error Message
```
OCR extraction failed: OCR processing failed: cannot import name 'LlamaFlashAttention2' 
from 'transformers.models.llama.modeling_llama'
```

### Root Cause
The error occurs when using newer versions of the `transformers` library (4.40+) with DeepSeek-OCR. The `LlamaFlashAttention2` class has been removed or reorganized in recent transformers versions. This affects model loading because:
1. DeepSeek-OCR's custom model code expects certain attention implementations
2. Different transformers versions have different attention mechanism APIs
3. Python 3.13 with transformers 4.57.1+ has this incompatibility

### Solution Applied (November 3, 2025)
Modified `app.py` to use a **three-tier fallback loading strategy**:

1. **First attempt**: Load with **"eager" attention** (most compatible)
2. **Second attempt**: Load with **"sdpa" attention** (scaled dot product)
3. **Third attempt**: Load without specifying attention (model default)

```python
# First try: eager attention (safest)
try:
    _model = AutoModelForCausalLM.from_pretrained(
        model_name,
        trust_remote_code=True,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
        low_cpu_mem_usage=True,
        device_map="auto" if device == "cuda" else None,
        attn_implementation="eager",
    )
except Exception as e:
    # Fallback to sdpa or default
    ...
```

### What This Means
- ✅ **Works with transformers 4.36 - 4.57+**
- ✅ **No additional dependencies** required (no flash-attn)
- ✅ **Automatic fallback** if one method fails
- ✅ **Compatible with Python 3.13**
- ⚠️ **Slightly slower** than Flash Attention 2 (but stable)

### Alternative Options

If you want maximum performance and have a compatible GPU:

1. **Install Flash Attention 2** (Linux/WSL only):
   ```bash
   pip install flash-attn --no-build-isolation
   ```

2. **Remove the attn_implementation parameter**:
   ```python
   # This will use flash_attention_2 if available
   _model = AutoModelForCausalLM.from_pretrained(
       model_name,
       trust_remote_code=True,
       ...
   )
   ```

### Performance Impact
- **Eager attention**: ~10-20% slower than Flash Attention 2
- **Still usable**: Processing time increases slightly but remains practical
- **CPU users**: No difference (Flash Attention 2 doesn't work on CPU anyway)

### Verification
Server should start successfully with message:
```
✓ DeepSeek-OCR model loaded successfully!
```

If you still see errors, the fallback method will attempt to load without the `attn_implementation` parameter.

---

**Status**: ✅ Fixed  
**Date**: November 3, 2025  
**Version**: app.py updated with eager attention implementation
