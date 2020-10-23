prev = [96, 104, 47, 106, 107, 108, 40, 110, 89, 61, 97, 94, 99, 100, 101, 102, 73, 74, 42, 76, 77, 43, 79, 80, 81, 82, 83, 84, 85, 60, 87, 88, 65, 66, 67, 45, 69, 70, 71, 72, 119, 120, 121, 122, 48, 49, 46, 51, 111, 126, 113, 114, 115, 116, 41, 118, 53, 44, 55, 62, 57, 56, 78, 105]
mapper = {}
#a1 = "^r8~UHE8O+llMklhIMl-JrErOFBaWGln+HdCJ-FyQ-=*TkFhIMlhIM+^IMlhI+xPLG8CWMl5LOxdck9q<thhIMlhQsU,ctxQ*HxBJtRrQEQ,SGYqMG~hIMlhIMl3IMlhILsGQ)8tTHI8c+8FTGI`"
#a1 = "^r8~UHE8O+llMklhIMl-JrErOFBaWGln+HdCJ-FyQ-=*TkFhIMlhIM+-IMlhI+EqS(BCTOJ0Oj=aSlEq<(,-TLE~QGtJT)=neOxBWL+vQGt-Uk9q<thhIMlhQsU,ctxQ*HxBJtRrQEQ,SGYqMG~hIMlhIM=vIMlhILsGQ)8tTHI8cLhXRO,E``"
#a1 = "^r8~UHE8O+llMklhIMl-JrErOFBaWGln+HdCJ-FyQ-=*TkFhIMlhIM+HIMlhIOd1+-=SOkx7OFQ,WGln+HdCI)BwRkB*SlEq<(~-TjFoQsdvR)dnePFEI)~rJn<hIMlYIHREcFR,Qr=wT(=nW(RRc-FzOFlhIMlhIO<hIMlh=Gd3<O,sfLlXRO,E``"
#a1 = "^r8~UHE8O+llMklhIMl-JrErOFBaWGln+HdCJ-FyQ-=*TkFhIMlhIM+dIMlhI+xPLG8CWM=3O+<eUFxPML<CILBhIMl/<)YrR(~-TE,3OF<5UtAqLHRSJt+hIMlhIMJhIMlhILs8=Gd3<O,sfL+XRO,E``"
#a1 = "Js+MY/+rYkBM+l`3c*5~jIxYTvdseC`FUosa+PdFUCthR)+.<jwA=PcAQ)81Un+sRPYd/Asa``??"     # header
#a1 = "Rv+FUvI" # guest
#a1 = "=PcAX/hoTv<FUHdwRO~0Y/t.TvhqT)RxT(MA^P<xTGJ3<vdsWO~FY(BxR(JFTA`?" # %s
#a1 = "<GlqYnh3<)+qU)BFT(~XQ)8ER*`8Y``?" # var power
#a1 = "Sv=BM/h3S(<.QP<^``"  # park kwangho
a1 = "eo`"

a2 = []
a3 = 1000
v5 = 0
v6 = 0
v7 = 0
v8 = 0

for i in a1:
    for j in range(64):
        if prev[j] == ord(i):
            v6 = j
            if v7 % 4 == 0:
                v7 += 1
            elif v7 % 4 == 1:
                if v8 < a3:
                    tmp = ((v6 & 0x30) >> 4) | 4 * v5
                    v8 += 1
                    v7 += 1
                    a2.append(chr(tmp))
            elif v7 % 4 == 2:
                if v8 < a3:
                    tmp = ((v6 & 0x3C) >> 2) | 16 * (v5 & 0xF)
                    v8 += 1
                    v7 += 1
                    a2.append(chr(tmp))
            elif v7 % 4 == 3:
                if v8 < a3:
                    tmp = v6 | ((v5 & 3) << 6)
                    v8 += 1
                    v7 += 1
                    a2.append(chr(tmp))
        v5 = v6

for i in a2:
    print(i, end = "")