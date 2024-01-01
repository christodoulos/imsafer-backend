function D = Scenes(s,file)
    if(s==1)
        [A,G,P, O,L] = scene1(file);
    elseif(s==2)
        [A,G,P, O,L] = scene2();
    elseif(s==3)
        [A,G,P, O,L] = scene3();
    elseif(s==4)
        [A,G,P, O,L] = scene4();
    elseif(s==5)
        [A,G,P, O,L] = scene5();
    else
        return;
    end
    
    % default alpha = 1
    init_struct = struct('type',0,'x',0,'y',0,'sigma',0,'sigma_x',0,'sigma_y',0,'alpha',1,'points',zeros(4,2));    
    obs = repmat(init_struct , size(O,1) , 1 );
    for i=1:size(O,1)
        obs(i).type = O(i,1);
        obs(i).x = O(i,2);
        obs(i).y = O(i,3);
        if(O(i,1) < 3 )
            obs(i).sigma_x = O(i,4);
            obs(i).sigma_y = O(i,5);
            obs(i).points(1,:) = [obs(i).x-obs(i).sigma_x obs(i).y-obs(i).sigma_y];
            obs(i).points(2,:) = [obs(i).x-obs(i).sigma_x obs(i).y+obs(i).sigma_y];
            obs(i).points(3,:) = [obs(i).x+obs(i).sigma_x obs(i).y-obs(i).sigma_y];
            obs(i).points(4,:) = [obs(i).x+obs(i).sigma_x obs(i).y+obs(i).sigma_y];
        elseif(O(i,1) == 3 )
            if( O(i,4) ~= O(i,5))
                disp('Nonequal size of a circle');
                return;
            end
            obs(i).sigma = O(i,4);
        else
            disp('Error obs type');
            return;
        end
    end

    init_struct = struct('pos',[],'fit',0);
    lights = repmat(init_struct , size(L,1) , 1 );
    for i=1:size(L,1)
        lights(i).pos = [L(i,1) L(i,2)];
        lights(i).fit = exp(sum((lights(i).pos - G).^2)/sum(A.^2))/exp(1);
    end
    
    D.Area = A;
    D.Goal = G;
    D.Pops = P;
    D.obs = obs;
    D.lights = lights;
end

function [Area, Goal, Pops, obs, light]=csvType2(M)
    Area = [M(1,1), M(1,3)];
    Goal = [M(2,1), M(2,3)];
    Pops = 40;
    obs = M(3:end,1:end);
    obs(:,1) = ones(size(obs,1),1);
    light = zeros(7,2);
    light(1,:) = Goal;
    for i=2:7
        ra = (Area(1)).*rand(10,1);
        rb = (Area(2)).*rand(10,1);
        light(i,1) = ra(i);
        light(i,2) = rb(i);
    end
end

function [Area, Goal, Pops, obs, light]=csvType1(M)
    Area = [M(1,2), M(1,3)];
    Goal = [M(2,2), M(2,3)];
    %light = Goal;
    light = M(1:end,6:7); 
    light = light(any(light,2),:);
    obs = M(10:end, 1:end);
    %Area = [600 400];
    %Goal = [30 11];
    Pops = M(1,4);
    % obs data array
    % type , center_x , center_y , half_width , half_hight
    % type = 1 -> wall
    % type = 2 -> retangle
    % type = 3 -> circle
    %{
    obs = [
        1   ,   300 ,   5   ,   300 ,   5 ;
        1   ,   300 ,   395 ,   300 ,   5;
        1   ,   5   ,   200 ,   5   ,   200;
        1   ,   595 ,   200 ,   5   ,   200;
                        
        2   ,   120   ,   320 ,   70   ,   40;
        2   ,   480   ,   80 ,   70   ,   40;
        
        2   ,   150   ,   80 ,   70   ,   40;
        2   ,   450   ,   320 ,   70   ,   40;
                
        2   ,   230   ,   180 ,   50   ,   40;
        2   ,   370   ,   220 ,   50   ,   40;
        
        2   ,   100   ,   200 ,   40   ,   40;
        2   ,   500   ,   200 ,   40   ,   40;
        
        3   ,   330   ,   90 ,   50   ,   50;
        3   ,   270   ,   310 ,   50   ,   50;

    ];

    % light point, the only light is exit
    light = [
        30  , 11;
    ];
    %}
end

function [Area, Goal, Pops, obs , light]=scene1(filename)    
    %filename = 'katoch.csv';
    M = csvread(filename);
    if M(1,1) == 0
        [Area, Goal, Pops, obs , light] = csvType1(M);
    else 
        [Area, Goal, Pops, obs , light] = csvType2(M);
    end
end