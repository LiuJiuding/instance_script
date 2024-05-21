#在当前位置创建渲染实例并把源物体移动到名为instance的空对象子级，集中管理源物体。如果不存在instace空对象则创建
import c4d
doc: c4d.documents.BaseDocument

doc.StartUndo()

srcobj = doc.GetActiveObject()
ins = c4d.BaseObject(5126)
ins.SetReferenceObject(srcobj)
ins.SetName(srcobj.GetName())
ins.SetMl(srcobj.GetMl())
ins[c4d.INSTANCEOBJECT_RENDERINSTANCE_MODE] = 1
ins.InsertAfter(srcobj)
doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, ins)#添加对象撤销在操作后进行

has_instance = False
objs = doc.GetObjects()
for obj in objs:
    if obj.GetName() == "instance_source":
        has_instance = True
        doc.AddUndo(c4d.UNDOTYPE_HIERARCHY_PSR,srcobj)
        srcobj.InsertUnder(obj)
        break
if has_instance == True:
    pass
else:
    nullobj = c4d.BaseObject(5140)
    nullobj.SetName("instance_source")
    doc.AddUndo(c4d.UNDOTYPE_HIERARCHY_PSR,srcobj)
    srcobj.InsertUnder(nullobj)
    doc.InsertObject(nullobj)
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ,nullobj)
c4d.EventAdd()
