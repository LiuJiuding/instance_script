#移动作为克隆的源物体到最上方，防止实例链接被破坏

import c4d
doc : c4d.documents.BaseDocument

obj = doc.GetActiveObject()
m = obj.GetMg()

doc.StartUndo()
doc.AddUndo(c4d.UNDOTYPE_HIERARCHY_PSR, obj)
obj.InsertBefore(doc.GetFirstObject())
obj.SetMg(m)
doc.EndUndo()

c4d.EventAdd()