; ModuleID = "programma"
target triple = "arm64-apple-darwin27.0.0"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

declare i32 @"scanf"(i8* %".1", ...)

define double @"al_dividi"(double %".1", double %".2")
{
entry:
  %"a" = alloca double
  store double %".1", double* %"a"
  %"b" = alloca double
  store double %".2", double* %"b"
  %".6" = load double, double* %"b"
  %".7" = fcmp oeq double %".6",              0x0
  br i1 %".7", label %"then", label %"else"
then:
  %".9" = call i32 (i8*, ...) @"printf"(i8* getelementptr ([4 x i8], [4 x i8]* @".str1", i32 0, i32 0), i8* getelementptr ([27 x i8], [27 x i8]* @".str0", i32 0, i32 0))
  ret double              0x0
else:
  br label %"endif"
endif:
  %".12" = load double, double* %"a"
  %".13" = load double, double* %"b"
  %".14" = fdiv double %".12", %".13"
  ret double %".14"
}

define double @"al_calcola"(i32 %".1", double %".2", double %".3")
{
entry:
  %"op" = alloca i32
  store i32 %".1", i32* %"op"
  %"a" = alloca double
  store double %".2", double* %"a"
  %"b" = alloca double
  store double %".3", double* %"b"
  %".8" = load i32, i32* %"op"
  %".9" = icmp eq i32 %".8", 1
  br i1 %".9", label %"then", label %"else"
then:
  %".11" = load double, double* %"a"
  %".12" = load double, double* %"b"
  %".13" = fadd double %".11", %".12"
  ret double %".13"
else:
  br label %"endif"
endif:
  %".16" = load i32, i32* %"op"
  %".17" = icmp eq i32 %".16", 2
  br i1 %".17", label %"then.1", label %"else.1"
then.1:
  %".19" = load double, double* %"a"
  %".20" = load double, double* %"b"
  %".21" = fsub double %".19", %".20"
  ret double %".21"
else.1:
  br label %"endif.1"
endif.1:
  %".24" = load i32, i32* %"op"
  %".25" = icmp eq i32 %".24", 3
  br i1 %".25", label %"then.2", label %"else.2"
then.2:
  %".27" = load double, double* %"a"
  %".28" = load double, double* %"b"
  %".29" = fmul double %".27", %".28"
  ret double %".29"
else.2:
  br label %"endif.2"
endif.2:
  %".32" = load double, double* %"a"
  %".33" = load double, double* %"b"
  %".34" = call double @"al_dividi"(double %".32", double %".33")
  ret double %".34"
}

define i32 @"main"()
{
entry:
  %"scelta" = alloca i32
  %"continua" = alloca i32
  %"x" = alloca double
  %"y" = alloca double
  store i32 0, i32* %"scelta"
  store i32 0, i32* %"continua"
  store double              0x0, double* %"x"
  store double              0x0, double* %"y"
  store i32 1, i32* %"continua"
  br label %"while_cond"
while_cond:
  %".8" = load i32, i32* %"continua"
  %".9" = icmp eq i32 %".8", 1
  br i1 %".9", label %"while_body", label %"endwhile"
while_body:
  %".11" = call i32 (i8*, ...) @"printf"(i8* getelementptr ([4 x i8], [4 x i8]* @".str1", i32 0, i32 0), i8* getelementptr ([56 x i8], [56 x i8]* @".str2", i32 0, i32 0))
  %".12" = call i32 (i8*, ...) @"scanf"(i8* getelementptr ([3 x i8], [3 x i8]* @".str3", i32 0, i32 0), i32* %"scelta")
  %".13" = call i32 (i8*, ...) @"printf"(i8* getelementptr ([4 x i8], [4 x i8]* @".str1", i32 0, i32 0), i8* getelementptr ([14 x i8], [14 x i8]* @".str4", i32 0, i32 0))
  %".14" = call i32 (i8*, ...) @"scanf"(i8* getelementptr ([4 x i8], [4 x i8]* @".str5", i32 0, i32 0), double* %"x")
  %".15" = call i32 (i8*, ...) @"printf"(i8* getelementptr ([4 x i8], [4 x i8]* @".str1", i32 0, i32 0), i8* getelementptr ([16 x i8], [16 x i8]* @".str6", i32 0, i32 0))
  %".16" = call i32 (i8*, ...) @"scanf"(i8* getelementptr ([4 x i8], [4 x i8]* @".str5", i32 0, i32 0), double* %"y")
  %".17" = call i32 (i8*, ...) @"printf"(i8* getelementptr ([4 x i8], [4 x i8]* @".str1", i32 0, i32 0), i8* getelementptr ([11 x i8], [11 x i8]* @".str7", i32 0, i32 0))
  %".18" = load i32, i32* %"scelta"
  %".19" = load double, double* %"x"
  %".20" = load double, double* %"y"
  %".21" = call double @"al_calcola"(i32 %".18", double %".19", double %".20")
  %".22" = call i32 (i8*, ...) @"printf"(i8* getelementptr ([4 x i8], [4 x i8]* @".str8", i32 0, i32 0), double %".21")
  %".23" = call i32 (i8*, ...) @"printf"(i8* getelementptr ([4 x i8], [4 x i8]* @".str1", i32 0, i32 0), i8* getelementptr ([27 x i8], [27 x i8]* @".str9", i32 0, i32 0))
  %".24" = call i32 (i8*, ...) @"scanf"(i8* getelementptr ([3 x i8], [3 x i8]* @".str3", i32 0, i32 0), i32* %"continua")
  br label %"while_cond"
endwhile:
  ret i32 0
}

@".str0" = internal constant [27 x i8] c"Errore: divisione per zero\00"
@".str1" = internal constant [4 x i8] c"%s\0a\00"
@".str2" = internal constant [56 x i8] c"1) Somma 2) Sottrazione 3) Moltiplicazione 4) Divisione\00"
@".str3" = internal constant [3 x i8] c"%d\00"
@".str4" = internal constant [14 x i8] c"Primo numero:\00"
@".str5" = internal constant [4 x i8] c"%lf\00"
@".str6" = internal constant [16 x i8] c"Secondo numero:\00"
@".str7" = internal constant [11 x i8] c"Risultato:\00"
@".str8" = internal constant [4 x i8] c"%g\0a\00"
@".str9" = internal constant [27 x i8] c"Continuare? 1 = si, 0 = no\00"