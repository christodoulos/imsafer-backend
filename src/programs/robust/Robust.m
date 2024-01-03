function Robust()

data = csvread('Data.csv');
plate.Data = data(3:end,:);
plate.CMx=data(1,1);
plate.CMy=data(1,2);
%% Problem Statement
ProblemParams.CostFuncName = 'distanceCV_CM';    % You should state the name of your cost function here.
ProblemParams.CostFuncExtraParams = plate;
% Parametroi pou prepei na bainoun exwterika....
ProblemParams.NPar = size(plate.Data, 1).*2;   % Number of optimization variables of your objective function. "NPar" is the dimention of the optimization problem.
ProblemParams.VarMin = [ 1 0.01  1 0.01  1 0.01  1 0.01  1 0.01  1 0.01  1 0.01  1 0.01]; % Lower limit of the optimization parameters. You can state the limit in two ways. 1)   2)
ProblemParams.VarMax = [11 0.04 14 0.04 14 0.04 14 0.04 14 0.04 14 0.04 11 0.04 14 0.04]; % Lower limit of the optimization parameters. You can state the limit in two ways. 1)   2)
[emin1, xmin1] = ImperialistCompetitveAlgorithm_GlobalOptimizationStrategy(ProblemParams);
if data(1,4) == 0 
    remove = 3;
else
    remove = data(1,4);
end
plate.Data(remove,:) = [];
if data(2,4) ~= 0 || data(2,5) ~= 0
    plate.CMx = data(2,1);
    plate.CMy = data(2,2);
end
[emin2, xmin2] = ImperialistCompetitveAlgorithm_GlobalOptimizationStrategy(ProblemParams);
savemin(emin1, xmin1, xmin2);
end

function savemin(emin, xmin1, xmin2)
    fw = fopen('run.res', 'w');
    wrpr('Optimum from empire algorithm', emin, xmin1, xmin2, fw);
    fclose(fw);
%     saveas(gcf(), 'run.jpg');
end


function wrpr(mes, emin, xmin1, xmin2, fw)
    fprintf('%s\n', mes);
    fprintf(fw, '%s\n', mes);
    fprintf('emin: %.15e\n', emin);
    fprintf(fw, 'emin: %.15e\n', emin);
    fprintf('xmin1:\n');
    fprintf(fw, 'xmin1:\n');
    for i=1:2:length(xmin1)
        fprintf('%10.3f%20.10e\n', xmin1(i), xmin1(i+1));
        fprintf(fw, '%10.3f%20.10e\n', xmin1(i), xmin1(i+1));
    end
    fprintf('xmin2:\n');
    fprintf(fw, 'xmin2:\n');
    for i=1:2:length(xmin2)
        fprintf('%10.3f%20.10e\n', xmin2(i), xmin2(i+1));
        fprintf(fw, '%10.3f%20.10e\n', xmin2(i), xmin2(i+1));
    end
end