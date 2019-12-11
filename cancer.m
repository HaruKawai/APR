addpath('~/asigDSIC/ETSINF/apr/bayes/BNT')
addpath(genpathKPM('~/asigDSIC/ETSINF/apr/bayes/BNT'))


%Ejercicio 6.10

N = 5; P = 1; F = 2; C = 3; R = 4; D = 5;

%Polucion: 1 = bajo, 2 = alto
%Fumador: 1 = false, 2 = true
%Cancer: 1 = false, 2 = true
%Rayos: 1 = false, 2 = dubte, 3 = true
%Disnea: 1 = false, 2 = true

grafo = zeros(N, N);
grafo(P,C) = 1;
grafo(F,C) = 1;
grafo(C,[R D]) = 1;

nodosDiscretos = 1:N;
tallaNodos = 2*ones(1,N); % [2 2 2 2 2]
tallaNodos(R) = 3;

redB = mk_bnet(grafo, tallaNodos, 'discrete', nodosDiscretos);

redB.CPD{P} = tabular_CPD(redB, P, [0.9 0.1]);
redB.CPD{F} = tabular_CPD(redB, F, [0.7 0.3]);
redB.CPD{C} = tabular_CPD(redB, C, [0.999 0.95 0.97 0.92 0.001 0.05 0.03 0.08]);

%TPC_R = zeros(2,2,3);
%TPC_R(1,1) = 0.8;
%TPC_R(1,2) = 0.1;
%TPC_R(1,3) = 0.1;
%TPC_R(2,1) = 0.1;
%TPC_R(2,2) = 0.2;
%TPC_R(2,3) = 0.7;

redB.CPD{R} = tabular_CPD(redB, R, [0.8 0.1 0.1 0.2 0.1 0.7]);
%redB.CPD{R} = tabular_CPD(redB, R, TPC_R);
redB.CPD{D} = tabular_CPD(redB, D, [0.7 0.35 0.3 0.65]);

motor = jtree_inf_engine(redB);

%(a)
evidencia = cell(1, N);
evidencia{F} = 1;
evidencia{R} = 1;
evidencia{D} = 2;
[motor, logVerosim] = enter_evidence(motor, evidencia);
m = marginal_nodes(motor, C);
m.T

%(b)
evidencia = cell(1, N);
evidencia{C} = 2;
[explMaxProb, logVerosim] = calc_mpe(motor, evidencia)


