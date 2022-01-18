% Ewout van Dartel
% 354720
% 3S project Bearing the Load

clc
clear

f1 = figure(9);
f2 = figure(10);

close([f1 f2])

% This script will plot the temperature lines of the tests.

fn0 = 'Sensor_output_12_01_2022_15_14_55_1199.9934';      % The file names can be coppied to here which will be read automatically
fn1 = 'Sensor_output_13_01_2022_11_30_46_1199.9922';      % in the following couple of lines in the for loop.
fn2 = 'Sensor_output_13_01_2022_12_53_05_1199.9967';      % Just coppying and pasting the filename makes it easy and quick.
fn3 = 'Sensor_output_13_01_2022_14_54_28_1199.9929';

z = (0:3);

for r = z
    filename = convertCharsToStrings(eval(sprintf('fn%d',r))); % chooses a filename depending on 0:3 and converts it to a string

    d = readtable(filename+'.csv');             % Defines the csv file and changes it to a table
    x12 = table2array(d(:,1));

    FilenameArray = split(filename,"_");        % The last value in the filename (fn 0 to 3) is the amount of time used collecting
    Time = str2double(FilenameArray(9,:));      % data. Because of synchronisation in the Arduino and the coding this is not a
    fs = ceil(length(x12)./Time);               % consistent process. So the amount of time meassured, and thus the sample
    L = length(x12);                            % frequency will not be the same for all tests. So these lines of codes are
    t1 = (0:L-1)./fs;                           % needed to calculate them for the FFT's. The filename is split in underscores

    x1 = zeros(1,length(x12));

    for b = 1:length(x12)
        if x12(b) > 1023
            x12(b) = 1023;
            x1(b) = 273.15;
        end

        R1 = 10000;
        c1 = 1.129252142e-03;
        c2 = 2.341083183e-04;
        c3 = 0.8773267909e-07;
        R2 = R1.*(1023./x12(b)-1);
        logR2 = reallog(R2);
        temper = 1./(c1+c2.*logR2+c3.*logR2.*logR2.*logR2);
        x1(b) = temper-273.15;

        if x1(b) < 0
            x1(b) = 0;
        end
    end
    
    Temp = movmean(x1,101);

    f1 = figure(9);                                   % Plotting the temperature of all 4 tests in 1 figure with it's maximum value
    hold on
    plot(t1,Temp,'DisplayName',['Test ' num2str(r+1) ' with max = ' num2str(max(Temp))])
    title('Temperatures of all tests with moving mean')
    xlabel('Time (s)')
    %ylim([-50 30])
    %xlim([0 1300])
    ylabel('Temperature (C)')

    f2 = figure(10);
    hold on
    plot(t1,x1,'DisplayName',['Test ' num2str(r+1) ' with max = ' num2str(max(Temp))])
    title('Temperatures of all tests without moving mean')
    xlabel('Time (s)')
    ylim([0 45])
    %xlim([0 1300])
    ylabel('Temperature (C)')

end

hold off
hold off

figure(9)
legend show

figure(10)
legend show


