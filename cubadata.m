
% Cuba 2.5ac vs. JMEC Electricity Data (2019-2025)

% Timeline
years = 2019:2025;

% JMEC Total Electricity Consumption (MWh)
JMEC = [119293.639, 31599.468, 68054.164, ...
    73430.865, 32401.281, 32506.292, NaN];

% Cuba 2.5ac Total Electricity Generation (MWh)
Cuba = [NaN, NaN, NaN, 4963, 6033, 5884, 5764];

TotalDemand = JMEC + Cuba;

% Create Graph
figure;

plot(years, JMEC, '-o', 'LineWidth', 2, ...
    'MarkerSize', 7);

hold on;

plot(years, Cuba, '-s', 'LineWidth', 2, ...
    'MarkerSize', 7);

plot(years, TotalDemand, '-^', 'LineWidth', 2, ...
    'MarkerSize', 7);

% Graph Formatting
title('Cuba 2.5ac Electricity Generation vs. JMEC Demand');

xlabel('Year');
ylabel('Electricity (MWh)');

legend('JMEC Total MWh', ...
    'Cuba 2.5ac Total Source', ...
    'Estimated Cuba Demand', ...
    'Location', 'best');

xticks(years);
xlim([2019 2025]);

grid on;
hold off;
