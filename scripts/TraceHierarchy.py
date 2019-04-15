# -----------------------------------------------------.
# シーン階層をたどる.
# -----------------------------------------------------.

scene = xshade.scene()

# 階層をたどる再帰.
def traceHierarchy (depth, shape):
  indentStr = "";
  for i in range(depth):
    indentStr += "    ";
  
  print indentStr + shape.name

  if shape.has_son:
    s = shape.son
    while s.has_bro:
      s = s.bro
      traceHierarchy(depth + 1, s)

# shapeから階層構造をたどって出力.
rootShape = scene.shape  # ルート形状.
traceHierarchy(0, rootShape)
