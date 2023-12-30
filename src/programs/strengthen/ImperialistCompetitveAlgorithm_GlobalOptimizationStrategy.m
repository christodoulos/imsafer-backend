function [empoptcost, empoptx] = ImperialistCompetitveAlgorithm_GlobalOptimizationStrategy(ProblemParams)
    %% Imperialist Competitive Algorithm (CCA);

    % A Socio Politically Inspired Optimization Strategy.
    % 2008

    % To use this code, you should only prepare your cost function and apply
    % CCA to it. Please read the guide available in my home page.

    % Special thank is for my friend Mostapha Kalami Heris whos breadth wision toward
    % artificial intelligence and his programming skils have always been a
    % sourse of inspiration for me. He helped me a lot to prepare this code.
    % His email: sm.kalami@gmail.com

    % ----------------------------------------
    % Esmaeil Atashpaz Gargari
    % Control and Intelligent Processing Center of Excellence,
    % ECE school of University of Tehran, Iran
    % Cellphone: (+98)-932-9011620
    % Email: e.atashpaz@ece.ut.ac.ir & atashpaz.gargari@gmail.com
    % Home Page: http://www.atashpaz.com

    function empfindopt(cost, x)  %Thanasis2021_12_25
        %Save minimum e and corresponding x.
        [costmin, imin] = min(cost);
        if costmin < empoptcost
            empoptcost = costmin;
            empoptx = x(imin, :);
        end
    end
    function empsavefigure() %Thanasis2021_12_29
        %Save current figure, so that the web interface will show it as the computation proceeds.
        %fn = sprintf('%s_r%03d.jpg', ProblemParams.CostFuncExtraParams.fpro, Decade);
        fn = sprintf('%s_r.jpg', ProblemParams.CostFuncExtraParams.fpro);
        delete(fn);     %delete dn, or else Matlab crashes (!!!) after some iterations.
        saveas(gcf(), fn);
    end

    % Modifying the size of VarMin and VarMax to have a general form
    if numel(ProblemParams.VarMin)==1
        ProblemParams.VarMin=repmat(ProblemParams.VarMin,1,ProblemParams.NPar);
        ProblemParams.VarMax=repmat(ProblemParams.VarMax,1,ProblemParams.NPar);
    end

    ProblemParams.SearchSpaceSize = ProblemParams.VarMax - ProblemParams.VarMin;

    %% Algorithmic Parameter Setting
    AlgorithmParams.NumOfCountries = 200;               % Number of initial countries.
    AlgorithmParams.NumOfInitialImperialists = 8;      % Number of Initial Imperialists.
    AlgorithmParams.NumOfAllColonies = AlgorithmParams.NumOfCountries - AlgorithmParams.NumOfInitialImperialists;
    AlgorithmParams.NumOfDecades = 40;
    AlgorithmParams.RevolutionRate = 0.3;               % Revolution is the process in which the socio-political characteristics of a country change suddenly.
    AlgorithmParams.AssimilationCoefficient = 2;        % In the original paper assimilation coefficient is shown by "beta".
    AlgorithmParams.AssimilationAngleCoefficient = .5;  % In the original paper assimilation angle coefficient is shown by "gama".
    AlgorithmParams.Zeta = 0.02;                        % Total Cost of Empire = Cost of Imperialist + Zeta * mean(Cost of All Colonies);
    AlgorithmParams.DampRatio = 0.99;
    AlgorithmParams.StopIfJustOneEmpire = false;         % Use "true" to stop the algorithm when just one empire is remaining. Use "false" to continue the algorithm.
    AlgorithmParams.UnitingThreshold = 0.02;            % The percent of Search Space Size, which enables the uniting process of two Empires.

    zarib = 1.05;                       % **** Zarib is used to prevent the weakest impire to have a probability equal to zero
    alpha = 0.1;                        % **** alpha is a number in the interval of [0 1] but alpha<<1. alpha denotes the importance of mean minimum compare to the global mimimum.

    %% Display Setting
    DisplayParams.PlotEmpires = false;    % "true" to plot. "false" to cancel ploting.
    if DisplayParams.PlotEmpires
        DisplayParams.EmpiresFigureHandle = figure('Name','Plot of Empires','NumberTitle','off');
        DisplayParams.EmpiresAxisHandle = axes;
    end

    DisplayParams.PlotCost = true;    % "true" to plot. "false"
    if DisplayParams.PlotCost
        DisplayParams.CostFigureHandle = figure('Name','Plot of Minimum and Mean Costs','NumberTitle','off');
        DisplayParams.CostAxisHandle = axes;
    end

    ColorMatrix = [1   0   0  ; 0 1   0    ; 0   0 1    ; 1   1   0  ; 1   0 1    ; 0 1   1    ; 1 1 1       ;
                   0.5 0.5 0.5; 0 0.5 0.5  ; 0.5 0 0.5  ; 0.5 0.5 0  ; 0.5 0 0    ; 0 0.5 0    ; 0 0 0.5     ;
                   1   0.5 1  ; 0.1*[1 1 1]; 0.2*[1 1 1]; 0.3*[1 1 1]; 0.4*[1 1 1]; 0.5*[1 1 1]; 0.6*[1 1 1]];
    DisplayParams.ColorMatrix = [ColorMatrix ; sqrt(ColorMatrix)];

    DisplayParams.AxisMargin.Min = ProblemParams.VarMin;
    DisplayParams.AxisMargin.Max = ProblemParams.VarMax;

    %% Creation of Initial Empires
    InitialCountries = GenerateNewCountry(AlgorithmParams.NumOfCountries , ProblemParams);

    % Calculates the cost of each country. The less the cost is, the more is the power.
    if isempty(ProblemParams.CostFuncExtraParams)
        InitialCost = feval(ProblemParams.CostFuncName,InitialCountries);
    else
        InitialCost = feval(ProblemParams.CostFuncName,InitialCountries,ProblemParams.CostFuncExtraParams);
    end
    [InitialCost,SortInd] = sort(InitialCost);                          % Sort the cost in assending order. The best countries will be in higher places
    InitialCountries = InitialCountries(SortInd,:);                     % Sort the population with respect to their cost.
    empoptcost = InitialCost(1);      %Thanasis2021_12_26: Initial optimum cost
    empoptx = InitialCountries(1, :); %Thanasis2021_12_26: x correspond to optimum cost

    Empires = CreateInitialEmpires(InitialCountries,InitialCost,AlgorithmParams, ProblemParams);

    %% Main Loop
    MinimumCost = repmat(nan,AlgorithmParams.NumOfDecades,1);
    MeanCost = repmat(nan,AlgorithmParams.NumOfDecades,1);

    if DisplayParams.PlotCost
        axes(DisplayParams.CostAxisHandle);
        if any(findall(0)==DisplayParams.CostFigureHandle)
            %h_MinCostPlot=plot(MinimumCost,'r','LineWidth',1.5,'YDataSource','MinimumCost');
            h_MinCostPlot=semilogy(MinimumCost,'r','LineWidth',1.5,'YDataSource','MinimumCost');  %Thanasis2021_12_25
            hold on;
            %h_MeanCostPlot=plot(MeanCost,'k:','LineWidth',1.5,'YDataSource','MeanCost');
            h_MeanCostPlot=semilogy(MeanCost,'k:','LineWidth',1.5,'YDataSource','MeanCost');   %Thanasis2021_12_25
            hold off;
            pause(0.05);
        end
    end

    for Decade = 1:AlgorithmParams.NumOfDecades
        AlgorithmParams.RevolutionRate = AlgorithmParams.DampRatio * AlgorithmParams.RevolutionRate;

        Remained = AlgorithmParams.NumOfDecades - Decade;
        fprintf('Current emin: %.15f    Remaining decades: %d\n', empoptcost, Remained);
        for ii = 1:numel(Empires)
            %% Assimilation;  Movement of Colonies Toward Imperialists (Assimilation Policy)
            Empires(ii) = AssimilateColonies(Empires(ii),AlgorithmParams,ProblemParams);

            %% Revolution;  A Sudden Change in the Socio-Political Characteristics
            Empires(ii) = RevolveColonies(Empires(ii),AlgorithmParams,ProblemParams);

            %% New Cost Evaluation
            if isempty(ProblemParams.CostFuncExtraParams)
                Empires(ii).ColoniesCost = feval(ProblemParams.CostFuncName,Empires(ii).ColoniesPosition);
            else
                Empires(ii).ColoniesCost = feval(ProblemParams.CostFuncName,Empires(ii).ColoniesPosition,ProblemParams.CostFuncExtraParams);
            end
            empfindopt(Empires(ii).ColoniesCost, Empires(ii).ColoniesPosition)  %Thanasis2021_12_25

            %% Empire Possession  (****** Power Possession, Empire Possession)
            Empires(ii) = PossesEmpire(Empires(ii));

            %% Computation of Total Cost for Empires
            Empires(ii).TotalCost = Empires(ii).ImperialistCost + AlgorithmParams.Zeta * mean(Empires(ii).ColoniesCost);

        end

        %% Uniting Similiar Empires
        Empires = UniteSimilarEmpires(Empires,AlgorithmParams,ProblemParams);

        %% Imperialistic Competition
        Empires = ImperialisticCompetition(Empires);

        if numel(Empires) == 1 && AlgorithmParams.StopIfJustOneEmpire
            break
        end

        %% Displaying the Results
        DisplayEmpires(Empires,AlgorithmParams,ProblemParams,DisplayParams);

        ImerialistCosts = [Empires.ImperialistCost];
        MinimumCost(Decade) = min(ImerialistCosts);
        MeanCost(Decade) = mean(ImerialistCosts);

        if DisplayParams.PlotCost
            refreshdata(h_MinCostPlot, 'caller');   %Thanasis2021_12_26: added 'caller'
            refreshdata(h_MeanCostPlot, 'caller');  %Thanasis2021_12_26: added 'caller'
            drawnow;
            empsavefigure(); %Thanasis2021_12_29
            pause(0.01);
        end

    end % End of Algorithm
    MinimumCost(end)
end


function NewCountry = GenerateNewCountry(NumOfCountries,ProblemParams)
    VarMinMatrix = repmat(ProblemParams.VarMin,NumOfCountries,1);
    VarMaxMatrix = repmat(ProblemParams.VarMax,NumOfCountries,1);

% Maria oi upoloipes grammes ftiaxnoun ton NewCountry me akeraious xoris round. Pare tis grammes autes
% kai valtes kai allou an xreiazontai.
    [m,n] = size(VarMaxMatrix);
    NewCountry = zeros(m,n);
    for i = 1:m
        for j = 1:n
            if mod(j,2)~= 0 % mones theseis (paxi mandya)
            NewCountry(i,j) = randi([VarMinMatrix(i,j),VarMaxMatrix(i,j)],1);
            else % zyges theseis (pososta oplismou)
                 NewCountry(i,j) = (VarMaxMatrix(i,j) - VarMinMatrix(i,j)) .* rand(1) + VarMinMatrix(i,j);
            end
        end
    end
end


function Empires = CreateInitialEmpires(InitialCountries,InitialCost,AlgorithmParams, ProblemParams)
    AllImperialistsPosition = InitialCountries(1:AlgorithmParams.NumOfInitialImperialists,:);
    AllImperialistsCost = InitialCost(1:AlgorithmParams.NumOfInitialImperialists,:);

    AllColoniesPosition = InitialCountries(AlgorithmParams.NumOfInitialImperialists+1:end,:);
    AllColoniesCost = InitialCost(AlgorithmParams.NumOfInitialImperialists+1:end,:);

    if max(AllImperialistsCost)>0
        AllImperialistsPower = 1.3 * max(AllImperialistsCost) - AllImperialistsCost;
    else
        AllImperialistsPower = 0.7 * max(AllImperialistsCost) - AllImperialistsCost;
    end

    AllImperialistNumOfColonies = round(AllImperialistsPower/sum(AllImperialistsPower) * AlgorithmParams.NumOfAllColonies);
    AllImperialistNumOfColonies(end) = AlgorithmParams.NumOfAllColonies - sum(AllImperialistNumOfColonies(1:end-1));
    RandomIndex = randperm(AlgorithmParams.NumOfAllColonies);

    Empires(AlgorithmParams.NumOfInitialImperialists).ImperialistPosition = 0;

    for ii = 1:AlgorithmParams.NumOfInitialImperialists
        Empires(ii).ImperialistPosition = AllImperialistsPosition(ii,:);
        Empires(ii).ImperialistCost = AllImperialistsCost(ii,:);
        R = RandomIndex(1:AllImperialistNumOfColonies(ii)); RandomIndex(AllImperialistNumOfColonies(ii)+1:end);
        Empires(ii).ColoniesPosition = AllColoniesPosition(R,:);
        Empires(ii).ColoniesCost = AllColoniesCost(R,:);
        Empires(ii).TotalCost = Empires(ii).ImperialistCost + AlgorithmParams.Zeta * mean(Empires(ii).ColoniesCost);
    end

    for ii = 1:numel(Empires)
        if numel(Empires(ii).ColoniesPosition) == 0
            Empires(ii).ColoniesPosition = GenerateNewCountry(1,ProblemParams);                 %
            Empires.ColoniesCost = feval(ProblemParams.FunctionName,Empires.ColoniesPosition);
        end
    end
end


function TheEmpire = AssimilateColonies(TheEmpire,AlgorithmParams,ProblemParams)
    % for i = 1:numel(Imperialists)
    %     Imperialists{i}.Number_of_Colonies_matrix = [Imperialists{i}.Number_of_Colonies_matrix      Imperialists{i}.Number_of_Colonies];
    %
    %     Imperialists_cost_matrix (i) = Imperialists{i}.cost_just_by_itself;
    %
    %     Imperialists_position_matrix(i,:) = Imperialists{i}.position;

    NumOfColonies = size(TheEmpire.ColoniesPosition,1);

    Vector = repmat(TheEmpire.ImperialistPosition,NumOfColonies,1)-TheEmpire.ColoniesPosition;

    [m,n] = size(Vector);
    for i = 1:m
        for j = 1:n
            if mod(j,2)~= 0 % mones theseis (paxi mandya)
                if Vector (i,j) < 0
                    TheEmpire.ColoniesPosition(i,j) = TheEmpire.ColoniesPosition(i,j) + 2 * AlgorithmParams.AssimilationCoefficient * randi([Vector(i,j),0],1) ;
                else
                    TheEmpire.ColoniesPosition(i,j) = TheEmpire.ColoniesPosition(i,j) + 2 * AlgorithmParams.AssimilationCoefficient * randi([0,Vector(i,j)],1) ;
                end
            else
                TheEmpire.ColoniesPosition(i,j) = TheEmpire.ColoniesPosition(i,j) + 2 * AlgorithmParams.AssimilationCoefficient * rand(1) .* Vector(i,j);
            end
        end
    end
    MinVarMatrix = repmat(ProblemParams.VarMin,NumOfColonies,1);
    MaxVarMatrix = repmat(ProblemParams.VarMax,NumOfColonies,1);

    TheEmpire.ColoniesPosition=max(TheEmpire.ColoniesPosition,MinVarMatrix);
    TheEmpire.ColoniesPosition=min(TheEmpire.ColoniesPosition,MaxVarMatrix);
end


function TheEmpire = RevolveColonies(TheEmpire,AlgorithmParams,ProblemParams)
    NumOfRevolvingColonies = round(AlgorithmParams.RevolutionRate * numel(TheEmpire.ColoniesCost));
    RevolvedPosition = GenerateNewCountry(NumOfRevolvingColonies , ProblemParams);
    R = randperm(numel(TheEmpire.ColoniesCost));
    R = R(1:NumOfRevolvingColonies);
    TheEmpire.ColoniesPosition(R,:) = RevolvedPosition;
end


function TheEmpire = PossesEmpire(TheEmpire)
    ColoniesCost = TheEmpire.ColoniesCost;

    [MinColoniesCost BestColonyInd]=min(ColoniesCost);
    if MinColoniesCost < TheEmpire.ImperialistCost

        OldImperialistPosition = TheEmpire.ImperialistPosition;
        OldImperialistCost = TheEmpire.ImperialistCost;

        TheEmpire.ImperialistPosition = TheEmpire.ColoniesPosition(BestColonyInd,:);
        TheEmpire.ImperialistCost = TheEmpire.ColoniesCost(BestColonyInd);

        TheEmpire.ColoniesPosition(BestColonyInd,:) = OldImperialistPosition;
        TheEmpire.ColoniesCost(BestColonyInd) = OldImperialistCost;
    end
end


function Empires=UniteSimilarEmpires(Empires,AlgorithmParams,ProblemParams)
    TheresholdDistance = AlgorithmParams.UnitingThreshold * norm(ProblemParams.SearchSpaceSize);
    NumOfEmpires = numel(Empires);

    for ii = 1:NumOfEmpires-1
        for jj = ii+1:NumOfEmpires
            DistanceVector = Empires(ii).ImperialistPosition - Empires(jj).ImperialistPosition;
            Distance = norm(DistanceVector);
            if Distance<=TheresholdDistance
                if Empires(ii).ImperialistCost < Empires(jj).ImperialistCost
                    BetterEmpireInd=ii;
                    WorseEmpireInd=jj;
                else
                    BetterEmpireInd=jj;
                    WorseEmpireInd=ii;
                end

                Empires(BetterEmpireInd).ColoniesPosition = [Empires(BetterEmpireInd).ColoniesPosition
                                                             Empires(WorseEmpireInd).ImperialistPosition
                                                             Empires(WorseEmpireInd).ColoniesPosition];

                Empires(BetterEmpireInd).ColoniesCost = [Empires(BetterEmpireInd).ColoniesCost
                                                         Empires(WorseEmpireInd).ImperialistCost
                                                         Empires(WorseEmpireInd).ColoniesCost];

                % Update TotalCost for new United Empire
                Empires(BetterEmpireInd).TotalCost = Empires(BetterEmpireInd).ImperialistCost + AlgorithmParams.Zeta * mean(Empires(BetterEmpireInd).ColoniesCost);

                Empires = Empires([1:WorseEmpireInd-1 WorseEmpireInd+1:end]);
                return;
            end
        end
    end
end


function Empires=ImperialisticCompetition(Empires)
    if rand > .11
        return
    end
    if numel(Empires)<=1
        return;
    end

    TotalCosts = [Empires.TotalCost];
    [MaxTotalCost WeakestEmpireInd] = max(TotalCosts);
    TotalPowers = MaxTotalCost - TotalCosts;
    PossessionProbability = TotalPowers / sum(TotalPowers);

    SelectedEmpireInd = SelectAnEmpire(PossessionProbability);

    nn = numel(Empires(WeakestEmpireInd).ColoniesCost);
    jj = myrandint(nn,1,1);

    Empires(SelectedEmpireInd).ColoniesPosition = [Empires(SelectedEmpireInd).ColoniesPosition
                                                   Empires(WeakestEmpireInd).ColoniesPosition(jj,:)];

    Empires(SelectedEmpireInd).ColoniesCost = [Empires(SelectedEmpireInd).ColoniesCost
                                               Empires(WeakestEmpireInd).ColoniesCost(jj)];

    Empires(WeakestEmpireInd).ColoniesPosition = Empires(WeakestEmpireInd).ColoniesPosition([1:jj-1 jj+1:end],:);
    Empires(WeakestEmpireInd).ColoniesCost = Empires(WeakestEmpireInd).ColoniesCost([1:jj-1 jj+1:end],:);

    %% Collapse of the the weakest colony-less Empire
    nn = numel(Empires(WeakestEmpireInd).ColoniesCost);
    if nn<=1
        Empires(SelectedEmpireInd).ColoniesPosition = [Empires(SelectedEmpireInd).ColoniesPosition
                                                       Empires(WeakestEmpireInd).ImperialistPosition];

        Empires(SelectedEmpireInd).ColoniesCost = [Empires(SelectedEmpireInd).ColoniesCost
                                                   Empires(WeakestEmpireInd).ImperialistCost];

        Empires=Empires([1:WeakestEmpireInd-1 WeakestEmpireInd+1:end]);
    end

end


function Index = SelectAnEmpire(Probability)
    R = rand(size(Probability));
    D = Probability - R;
    [MaxD Index] = max(D);
end


function y = myrandint(MaxInt,m,n)
    %function y = myrandint(MaxInt,m,n)
    % This functions creates random numbers between [1 MaxInt] (1 itself and MaxInt itself)
    if nargin == 1
        y = ceil(rand*MaxInt);
    elseif nargin == 3
        y = ceil(rand(m,n)*MaxInt);
    else
        warning('Incorrect Number of Inputs');
    end
end


function DisplayEmpires(Empires,AlgorithmParams,ProblemParams,DisplayParams)
    if ~DisplayParams.PlotEmpires
        return;
    end

    if (ProblemParams.NPar ~= 2) && (ProblemParams.NPar ~= 3)
        return;
    end

    if ~any(findall(0)==DisplayParams.EmpiresFigureHandle)
        return;
    end


    if ProblemParams.NPar == 2
        for ii = 1:numel(Empires)
            plot(DisplayParams.EmpiresAxisHandle,Empires(ii).ImperialistPosition(1),Empires(ii).ImperialistPosition(2),'p',...
                'MarkerEdgeColor','k',...
                'MarkerFaceColor',DisplayParams.ColorMatrix(ii,:),...
                'MarkerSize',70*numel(Empires(ii).ColoniesCost)/AlgorithmParams.NumOfAllColonies + 13);
            hold on

            plot(DisplayParams.EmpiresAxisHandle,Empires(ii).ColoniesPosition(:,1),Empires(ii).ColoniesPosition(:,2),'ok',...
                'MarkerEdgeColor','k',...
                'MarkerFaceColor',DisplayParams.ColorMatrix(ii,:),...
                'MarkerSize',8);
        end

        xlim([DisplayParams.AxisMargin.Min(1) DisplayParams.AxisMargin.Max(1)]);
        ylim([DisplayParams.AxisMargin.Min(2) DisplayParams.AxisMargin.Max(2)]);
        hold off
    end

    if  ProblemParams.NPar == 3
        figure(1)
        for ii = 1:numel(Empires)
            plot3(DisplayParams.EmpiresAxisHandle,Empires(ii).ImperialistPosition(1),Empires(ii).ImperialistPosition(2),Empires(ii).ImperialistPosition(3),'p',...
                'MarkerEdgeColor','k',...
                'MarkerFaceColor',DisplayParams.ColorMatrix(ii,:),...
                'MarkerSize',70*numel(Empires(ii).ColoniesCost)/AlgorithmParams.NumOfAllColonies + 13);
            hold on

            plot3(DisplayParams.EmpiresAxisHandle,Empires(ii).ColoniesPosition(:,1),Empires(ii).ColoniesPosition(:,2),Empires(ii).ColoniesPosition(:,3),'ok',...
                'MarkerEdgeColor','k',...
                'MarkerFaceColor',DisplayParams.ColorMatrix(ii,:),...
                'MarkerSize',8);
        end

        xlim([DisplayParams.AxisMargin.Min(1) DisplayParams.AxisMargin.Max(1)]);
        ylim([DisplayParams.AxisMargin.Min(2) DisplayParams.AxisMargin.Max(2)]);
        zlim([DisplayParams.AxisMargin.Min(3) DisplayParams.AxisMargin.Max(3)]);
        hold off
    end

    pause(0.05);
end
