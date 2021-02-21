from cmath import sqrt
# ax^2+bx+c=0
print('本程序用公式解二次方程')
print('输入ax^2+bx+c=0中的a,b,c,一行一个，输完回车自动输出结果')
print('如果给以无解参数会出bug')
a = int(input())
b = int(input())
c = int(input())

print((-b+sqrt(b**2-4*a*c).real)/(2*a))
print((-b-sqrt(b**2-4*a*c).real)/(2*a))