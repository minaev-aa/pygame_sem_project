from settings import *
wait = 200
frequency_list = [3.505, 3.515, 3.522, 3.532, 3.535, 3.542, 3.552, 3.555, 3.565, 3.572, 3.575, 3.582, 3.592, 3.595, 3.600]
A = '._'
B = '_...'
C = '_._.'
D = '_..'
E = '.'
F = '.._.'
G = '__.'
H = '....'
I = '..'
J = '.___'
K = '_._'
L = '._..'
M = '__'
N = '_.'
O = '___'
P = '.__.'
Q = '__._'
R = '._.'
S = '...'
T = '_'
U = '.._'
V = '..._'
W = '.__'
X = '_.._'
Y = '_.__'
Z = '__..'
words = [[S, H, E, L, L], [H, A, L, L, S], [S, L, I, C, K], [T, R, I, C, K], [B, O, X, E, S], [L, E, A, K, S], \
         [S, T, R, O, B, E], [B, I, S, T, R, O], [F, L, I, C, K], [B, O, M, B, S], [B, R, E, A, K], [B, R, I, C, K], \
         [S, T, E, A, K], [S, T, I, C, K], [V, E, C, T, O, R], [B, E, A, T, S]]
top_end = (3 * width_screen//10, 8 * height_screen//10)
size_end = (4 * width_screen//10, 1 * height_screen//10)