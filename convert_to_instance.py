#将选定对象转化为实例并删除，变化矩阵相同，以最后一个选择对象为源

import c4d
doc: c4d.documents.BaseDocument

objs = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
srcobj = objs[-1]

doc.StartUndo()
for i in range(len(objs)-1):
    ins = c4d.BaseObject(5126)
    ins.SetReferenceObject(srcobj)
    ins.SetName(srcobj.GetName())
    ins.SetMl(objs[i].GetMl())
    ins.InsertAfter(objs[i])
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, ins)#添加对象撤销在操作后进行

for i in range(len(objs)-1):
    doc.AddUndo(c4d.UNDOTYPE_DELETEOBJ, objs[i])#删除对象撤销在操作前进行
    objs[i].Remove()
doc.EndUndo()
c4d.EventAdd()