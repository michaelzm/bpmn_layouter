import sys
print("Python Executable:", sys.executable)
print("sys.path:")
for p in sys.path:
    print("  ", p)

try:
    import graphviz
    print("✅ graphviz imported successfully!")
except ImportError as e:
    print("❌ ImportError:", e)