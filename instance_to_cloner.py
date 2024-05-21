# 选中多重实例模式的实例对象，转化为克隆
import c4d
doc: c4d.documents.BaseDocument # The document evaluating this effector

def CreateMesh(mtx) ->c4d.BaseObject:
    mesh = c4d.BaseObject(5100)
    pos = []
    for i in mtx:
        pos.append(i.off)
    mesh.ResizeObject(len(pos))
    mesh.SetAllPoints(pos)
    mesh.Message(c4d.MSG_UPDATE)
    return mesh

def Matrix2String(mtx):
    
    mtxstr = "{:.10f}".format(mtx.v1[0]) + " " + "{:.10f}".format(mtx.v1[1]) + " " + "{:.10f}".format(mtx.v1[2]) + " " + "{:.10f}".format(mtx.v2[0]) + " " + "{:.10f}".format(mtx.v2[1]) + " " + "{:.10f}".format(mtx.v2[2]) + " " + "{:.10f}".format(mtx.v3[0]) + " " + "{:.10f}".format(mtx.v3[1]) + " " + "{:.10f}".format(mtx.v3[2]) + " " + "{:.10f}".format(mtx.off[0]) + " " + "{:.10f}".format(mtx.off[1]) + " " + "{:.10f}".format(mtx.off[2]) + " "
    return mtxstr

def main():
    obj = doc.GetActiveObject()
    # check type is instance and in multi mode
    if obj.GetType() == 5126:
        if obj[c4d.INSTANCEOBJECT_RENDERINSTANCE_MODE] == 2:
            
            nullobj = c4d.BaseObject(5140)
            nullobj.SetName(obj.GetName())
            srcobj = obj.GetReferenceObject(doc)
            mtx = obj.GetInstanceMatrices()

            # add instance to source obj
            ins = c4d.BaseObject(5126)
            ins[c4d.INSTANCEOBJECT_RENDERINSTANCE_MODE] = 0
            ins.SetReferenceObject(srcobj)
            ins.SetName(obj.GetName())

            # set mesh and cloner
            mesh = CreateMesh(mtx)
            mesh.SetName(obj.GetName()+"_pos")
            cloner = c4d.BaseObject(1018544)
            
            cloner[c4d.ID_MG_MOTIONGENERATOR_MODE] = 0
            cloner[c4d.MG_OBJECT_LINK] = mesh
            cloner[c4d.MG_POLY_MODE_] = 0
            cloner[c4d.MG_OBJECT_ALIGN] = 0
            cloner[c4d.MGCLONER_VOLUMEINSTANCES_MODE] = 2
            cloner.SetName(obj.GetName())

            # add python effector
            py = c4d.BaseObject(1025800)
            py.SetName(obj.GetName()+"_py")
            inExcludeData = cloner[c4d.ID_MG_MOTIONGENERATOR_EFFECTORLIST]
            inExcludeData.InsertObject(py, 1)
            cloner[c4d.ID_MG_MOTIONGENERATOR_EFFECTORLIST] = inExcludeData

            # add userdata
            bc = c4d.GetCustomDataTypeDefault(c4d.DTYPE_STRING)
            bc[c4d.DESC_NAME] = "mtx"
            descId = py.AddUserData(bc)
            mtxstr = ''
            for i in mtx:
                mtxstr += Matrix2String(i)
            py[descId] = mtxstr

            # set python code
            py[c4d.OEPYTHON_MODE] = 1
            py[c4d.OEPYTHON_STRING] = '''
# test
import c4d

op: c4d.BaseObject # The python effector
gen: c4d.BaseObject # The MoGraph Generator executing the effector
doc: c4d.documents.BaseDocument # The document evaluating this effector
thread: c4d.threading.BaseThread # The thread executing this effector

def String2Matrix(mtxstr):
    s = mtxstr.split()
    mtx = []
    for i in range(int(len(s)/12)):
        m = c4d.Matrix()
        m.v1 = c4d.Vector(float(s[12*i]),float(s[12*i+1]),float(s[12*i+2]))
        m.v2 = c4d.Vector(float(s[12*i+3]),float(s[12*i+4]),float(s[12*i+5]))
        m.v3 = c4d.Vector(float(s[12*i+6]),float(s[12*i+7]),float(s[12*i+8]))
        m.off = c4d.Vector(float(s[12*i+9]),float(s[12*i+10]),float(s[12*i+11]))
        mtx.append(m)
    return mtx

def main() -> bool:

    # Called when the effector is executed to set MoGraph data. Similar to EffectorData::ModifyObject in C++.
    moData = c4d.modules.mograph.GeGetMoData(op)

    if moData is None:
        return False

    cnt = moData.GetCount()
    marr = moData.GetArray(c4d.MODATA_MATRIX)

    hasField = op[c4d.FIELDS].HasContent()
    fall = moData.GetFalloffs()

    mtx = String2Matrix(op[c4d.ID_USERDATA,1])
    for i in range(0, cnt):
        marr[i].v1 = mtx[i].v1
        marr[i].v2 = mtx[i].v2
        marr[i].v3 = mtx[i].v3
    moData.SetArray(c4d.MODATA_MATRIX, marr, hasField)
    return True'''

            # assamble objs
            doc.StartUndo()
            py.InsertUnder(nullobj)
            doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, py)#添加对象撤销在操作后进行
            mesh.InsertUnder(nullobj)
            doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, mesh)#添加对象撤销在操作后进行
            ins.InsertUnder(cloner)
            doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, ins)#添加对象撤销在操作后进行
            cloner.InsertUnder(nullobj)
            doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, cloner)#添加对象撤销在操作后进行
            doc.InsertObject(nullobj)
            doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, nullobj)#添加对象撤销在操作后进行
            c4d.EventAdd()

if __name__ == '__main__':
    main()

