function optimeccentricity(fpro)
    [results, plate, tmax, rhomm] = readData(fpro);
    [varmin, varmax] = minmax(plate.Data, tmax, rhomm);

    %% Problem Statement
    ProblemParams.CostFuncName = 'distanceCV_CM';    % You should state the name of your cost function here.
    ProblemParams.CostFuncExtraParams = plate;
    % Parametroi pou prepei na bainoun exwterika....
    ProblemParams.NPar = size(plate.Data, 1).*2;   % Number of optimization variables of your objective function. "NPar" is the dimention of the optimization problem.
    ProblemParams.VarMin = varmin; % Lower limit of the optimization parameters. You can state the limit in two ways. 1)   2)
    ProblemParams.VarMax = varmax; % Lower limit of the optimization parameters. You can state the limit in two ways. 1)   2)
    [emin, xmin] = ImperialistCompetitveAlgorithm_GlobalOptimizationStrategy(ProblemParams);
    savemin(fpro, results, plate.Data, emin, xmin); %Thanasis2021_12_25
end


function [temp, plate, tmax, rhomm] = readData(fpro)
    %Read the parameters of the problem and the optimization.
    plate.fpro = fpro;   %In irder to save graphs at every iteration
    fn = [fpro '.csv'];
    temp = csvread(fn);
    plate.CMx=temp(1, 1);
    plate.CMy=temp(1, 2);
    rhomm = temp(2, 1:2);
    plate.Data = temp(3:end, 1:14);
    tmax = temp(3:end, 15)';
end


function [varmin, varmax] = minmax(Data, tmax, rhomm)
    %Compute the min/max of the design variables; convert tmax from cm to m.
    n = size(Data, 1);
    varmin = zeros(1, 2*n);
    varmax = zeros(1, 2*n);
    tmax = convert2cm(Data, tmax);
    for i=1:n
        varmin(2*i-1) = 1;
        varmax(2*i-1) = tmax(i);
        varmin(2*i) = rhomm(1);
        varmax(2*i) = rhomm(2);
    end
end


function tmax=convert2cm(Data, tmax)
    %The max thickness of the additional mantle is converted to the crazy integer cm used
    %by the optimization crazy algorithm.
    %It is the inverse of convert2m(), with rounding.
    for i=1:length(tmax)
        if Data(i,7)==0 && tmax(i)~=0.0
            %t(i) = 0.08 + (t(i)-2)*0.01; % μη ενισχυμένα αρχικώς υποστυλώματα
            %t(i)-0.08 = (t(i)-2)*0.01
            %t(i)-0.08)*100 = t(i)-2 =>
            tmax(i) = round((tmax(i)-0.08)*100 + 2);
            tmax(i) = max(tmax(i), 2);
        elseif Data(i,7)~=0 && tmax(i)~=0.0
            %t(i) = 0.01 + (t(i)-2)*0.01;  % ενισχυμένα αρχικώς υποστυλώματα
            %t(i) - 0.01 = (t(i)-2)*0.01
            %(t(i) - 0.01)*100 = t(i)-2
            tmax(i) = round((tmax(i)-0.01)*100 + 2);
            tmax(i) = max(tmax(i), 2);
        else
            tmax(i)=1;  %This means zero!
        end
    end
end


function t=convert2m(Data, t)
    %After the optimization the thickness of the additional mantle is converted to m:
    %a. If the initial mantle thickness is zero and the thickness of the additional
    %   mantle is not 1 (which means that is not zero or less - note that the thickness
    %   can not be < 1), which also means that it is at least 2:
    %   t = 0.08 + (t-2)*0.01;  % μη ενισχυμένα αρχικώς υποστυλώματα
    %b. If the initial mantle thickness is not zero m (i.e. > zero m) and the thickness
    %   of the additional mantle is not 1, which also means that it is at least 2:
    %   t = 0.01 + (t-2)*0.01;  % ενισχυμένα αρχικώς υποστυλώματα
    %c. Else (i.e. the thickness of the additional mantle is 1):
    %   t = 0.0
    for i=1:length(t)
        if Data(i,7)== 0 && t(i) ~= 1
            t(i) = 0.08 + (t(i)-2)*0.01; % μη ενισχυμένα αρχικώς υποστυλώματα
        elseif Data(i,7)~=0 && t(i) ~= 1
            t(i) = 0.01 + (t(i)-2)*0.01;  % ενισχυμένα αρχικώς υποστυλώματα
        else
            t(i)=0;
        end
    end
end


function savemin(fpro, results, Data, emin, xmin)
    %Save and print the results in various formats.
    t = xmin(1:2:end);
    rho = xmin(2:2:end);
    t = convert2m(Data, t);
    fn = [fpro '_r.txt'];
    fw = fopen(fn, 'w');
    wrpr('Optimum from empire algorithm', emin, t, rho, fw);
    fclose(fw);

    results(3:end, 9) = t;
    results(3:end, 10) = rho;
    fn = [fpro '_r.csv'];
    dlmwrite(fn, results, 'precision', 15);

    %fn = [fpro '_r.jpg'];
    %saveas(gcf(), fn);      %Already saved by ImperialistCompetitveAlgorithm_GlobalOptimizationStrategy()
end


function wrpr(mes, emin, t, rho, fw)
    %Save in text file and print to screen.
    fprintf('%s\n', mes);
    fprintf(fw, '%s\n', mes);
    fprintf('emin: %.15e\n', emin);
    fprintf(fw, 'emin: %.15e\n', emin);
    fprintf('xmin:\n');
    fprintf(fw, 'xmin:\n');

    fprintf(' t_new (m)   reinforcement rho\n');
    fprintf(fw, ' t_new (m)   reinforcement rho\n');
    for i=1:length(t)
        fprintf('%10.3f%20.10e\n', t(i), rho(i));
        fprintf(fw, '%10.3f%20.10e\n', t(i), rho(i));
    end
end
