addpath('~/asigDSIC/ETSINF/apr/bayes/BNT')
addpath(genpathKPM('~/asigDSIC/ETSINF/apr/bayes/BNT'))

%Sprinkler
N = 4; C = 1; S = 2; R = 3; W = 4;

grafo = zeros(N, N);
grafo(C,[R S]) = 1;
grafo(R,W) = 1;
grafo(S,W) = 1;

nodosDiscretos = 1:N;
tallaNodos = 2*ones(1,N);

redB = mk_bnet(grafo, tallaNodos, 'discrete', nodosDiscretos);

TPC_W = zeros(2, 2, 2);
redB.CPD{W} = tabular_CPD(redB, W, [1.0 0.1 0.1 0.01 0.0 0.9 0.9 0.99]);
redB.CPD{C} = tabular_CPD(redB, C, [0.5 0.5]);
redB.CPD{S} = tabular_CPD(redB, S, [0.5 0.9 0.5 0.1]);
redB.CPD{R} = tabular_CPD(redB, R, [0.8 0.2 0.2 0.8]);

motor = jtree_inf_engine(redB);
evidencia = cell(1, N);

%Ejercicio 1
  %Con datos completos
semilla = 0; rng(semilla);
nMuestras = 1000;
muestras = cell(N, nMuestras);
for i=1:nMuestras muestras(:,i) = sample_bnet(redB); end
%muestras'

redAPR = mk_bnet(grafo, tallaNodos);
redAPR.CPD{C} = tabular_CPD(redAPR, C);
redAPR.CPD{R} = tabular_CPD(redAPR, R);
redAPR.CPD{S} = tabular_CPD(redAPR, S);
redAPR.CPD{W} = tabular_CPD(redAPR, W);

redAPR2=learn_params(redAPR, muestras);

TPCaux = cell(1,N);
for i=1:N s=struct(redAPR2.CPD{i}); TPCaux{i}=s.CPT; end

dispcpt(TPCaux{W}) %probabilidad estimada para el nodo w

  %con datos incompletos
muestrasS = muestras;
semilla = 0; rng(semilla);
ocultas = rand(N, nMuestras) > 0.5;
[I,J] = find(ocultas);
for k=1:length(I) muestrasS{I(k), J(k)} = []; end
%muestrasS' %comprobamos que datos se han ocultado

%nueva red
redEM = mk_bnet(grafo, tallaNodos, 'discrete', nodosDiscretos);
redEM.CPD{C} = tabular_CPD(redEM, C);
redEM.CPD{R} = tabular_CPD(redEM, R);
redEM.CPD{S} = tabular_CPD(redEM, S);
redEM.CPD{W} = tabular_CPD(redEM, W);
motorEM = jtree_inf_engine(redEM);

%aprendizaje
maxIter = 1000; eps = 1e-10;
semilla = 0; rng(semilla);
[redEM2, trazaLogVer] = learn_params_em(motorEM, muestrasS, maxIter, eps);
auxTPC = cell(1,N);
for i=1:N s=struct(redEM2.CPD{i}); auxTPC{i}=s.CPT; end

dispcpt(auxTPC{W})  %probabilidad estimada para el nod s tras 20 iteraciones


