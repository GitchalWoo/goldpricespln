# Python Style Guide - GoldPrice Project

## Critical Rule: No Emojis in Python Scripts

**IMPORTANT**: Never add emojis to Python scripts. Use text-based counterparts instead.

### Reason
Emojis in Python source code can cause:
- Encoding issues on different platforms
- Display problems in terminals and editors
- Confusion when reviewing code
- Difficulty searching for specific patterns
- Potential compatibility issues with build systems

### Approved Text Alternatives

Replace emojis with these text-based alternatives:

| Emoji | Use Instead | Context |
|-------|------------|---------|
| 📊 | [DATA] | Data-related messages |
| 🔄 | [RUN] | Running/processing scripts |
| ✅ | [OK] | Success/completion |
| ⚠️ | [WARN] | Warnings |
| ❌ | [ABORT] or [ERROR] | Errors/failures |
| ✨ | [DONE] | Done/finished |
| 📍 | [STEP-#] | Step markers |
| 📥 | [INBOX] | Input/incoming data |
| 📈 | [GRAPH] | Graphs/charts/data analysis |
| 💰 | [MONEY] | Currency/financial data |
| 🔗 | [LINK] | Linking/combining data |
| 📁 | [FILES] | File operations |
| 🏠 | [HOUSE] | Real estate/housing |
| 💾 | [SAVE] | Saving data |
| 🌐 | [WEB] | Network/web operations |
| 📁 | [FOLDER] | Folder operations |

### Examples

❌ **Bad:**
```python
print(f"🔄 Running: {description}")
print(f"✅ Completed successfully!")
print(f"📊 Data Summary:")
```

✅ **Good:**
```python
print(f"[RUN] Running: {description}")
print(f"[OK] Completed successfully!")
print(f"[DATA] Data Summary:")
```

### Where This Applies
- Python script files (`.py`)
- Python docstrings and comments
- Print statements and logging
- All user-facing output

### Where Emojis Are OK
- Documentation files (Markdown, README)
- Issue descriptions and comments
- Git commit messages (optional)
- Non-Python configuration files

---

**Last Updated**: October 19, 2025
