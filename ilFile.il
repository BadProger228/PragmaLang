.assembly solve {}
.method public static void Main(){
.entrypoint
.locals init (
float32 a,
float32 b,
float32 c,
float32 z
)
    ldc.r4 19.0
    stloc.0
    ldc.r4 17.0
    stloc.1
    ldloc.0
    ldloc.1
    add
    ldc.r4 14.0
    sub
    stloc.2
    ldloc.0
    ldloc.2
    add
    ldloc.1
    cgt
    brfalse.s m0
    ldloc.2
    ldloc.1
    add
    stloc.0
    ldc.r4 18.0
    stloc.3
    br.s m1
m0:
    ldloc.2
    ldloc.1
    sub
    stloc.0
m1:ret
}