% Ewout van Dartel
% 354720
% 3S project Bearing the Load

clc
clear

% This script will plot the self gathered data.

% Defining the data Collumns of the csv-file:                                             
% 1 = Temperature
% 2 = Accelerometer horizontal (top)
% 3 = Accelerometer vertical (bottom)
% 4 = Microphone (top-left)
% 5 = Microphone (top-right)
% 6 = Microphone (bottom)

fn0 = 'Sensor_output_12_01_2022_15_14_55_1199.9934';      % The file names can be coppied to here which will be read automatically
fn1 = 'Sensor_output_13_01_2022_11_30_46_1199.9922';      % in the following couple of lines in the for loop.
fn2 = 'Sensor_output_13_01_2022_12_53_05_1199.9967';      % Just coppying and pasting the filename makes it easy and quick.
fn3 = 'Sensor_output_18_01_2022_10_47_49_1199.998';

% Sensor_output_12_01_2022_15_14_55_1199.9934       Test 1
% Sensor_output_13_01_2022_11_30_46_1199.9922       Test 2
% Sensor_output_13_01_2022_12_53_05_1199.9967       Test 3
% Sensor_output_13_01_2022_14_54_28_1199.9929       Test 4
% Sensor_output_18_01_2022_10_47_49_1199.998        Test 4 2

z=(0:3);    % Defining the numbers for the for loop where all 4 test data sets will be read and plotted. Memory issues so only 1 at
% a time ended up to be possible for my laptop.
for r = z                                   % The for loop to do all analysing of all four tests in one go
    filename = convertCharsToStrings(eval(sprintf('fn%d',r))); % chooses a filename depending on 0:3 and converts it to a string

    d = readtable(filename+'.csv');         % Defines the csv file and changes it to a table
    x12 = table2array(d(:,1));              % Assigning every collumn of the csv file to a new variable
    x22 = table2array(d(:,2))./1023.*3.3;   % The analog signals of the accelerometers and the microphones will be
    x32 = table2array(d(:,3))./1023.*3.3;   % devided by 1023 and multiplied by 3.3 to convert the unitless digital signal
    x42 = table2array(d(:,4))./1023.*3.3;   % to a voltage in Volts. The calculations for the temperature data are done
    x52 = table2array(d(:,5))./1023.*3.3;   % in the first section below.
    x62 = table2array(d(:,6))./1023.*3.3;
    
%     x22 = x22-mean(x22);        % The baseline of the signal is not at 0 Volts. There is a constant in the signal which the FFT
%     x32 = x32-mean(x32);        % will see as a wave with a frequency close to zero. Because the value or amplitude of this wave
%     x42 = x42-mean(x42);        % is way higher than the amplitude of the actual signal, the FFT will give (compared to the others)
%     x52 = x52-mean(x52);        % an enormous peak at close to 0 Hz which makes the other vibration invisible. To reduce this
%     x62 = x62-mean(x62);        % occurance the mean of the signal is deducted from the actual signal so the baseline is somewhat
    x72 = mean([x42, x52, x62],2);      % close to zero.

    FilenameArray = split(filename,"_");    % The last value in the filename (fn 0 to 3) is the amount of time used collecting
    Time = str2double(FilenameArray(9,:));  % data. Because of synchronisation in the Arduino and the coding this is not a
    fs = ceil(length(x12)./Time);           % consistent process. So the amount of time meassured, and thus the sample
    L = length(x12);                        % frequency will not be the same for all tests. So these lines of codes are
    t1 = (0:L-1)./fs;                       % needed to calculate them for the FFT's. The filename is split in underscores

    if Time > 10                            % Measuring time is 20 minutes, 1200 seconds. To reduce the used and workspace
        x2 = x22(1:(10*fs));                % memory it is chosen to apply the FFT only on the first 10 seconds.
        x3 = x32(1:(10*fs));                % Because the damages to the bearings are done by hand the generated vibrations
        x4 = x42(1:(10*fs));                % by the bearings should not change in 20 minutes of time because of its long
        x5 = x52(1:(10*fs));                % lifespan. This means that a FFT of the first 10 seconds is accurate is well.
        x6 = x62(1:(10*fs));                % This is also reduces the peak close to 0 Hz as discussed at line 38-43.
    else
        x2 = x22;
        x3 = x32;
        x4 = x42;
        x5 = x52;
        x6 = x62;
    end   

%% First section, plot the temperature (x1)

    x1 = zeros(1,length(x12));              % Generating an array to reduce the RAM memory because the temperature calculations
% generate an array which gets bigger after every for-loop.
    for b = 1:length(x12)                   % For loop to do the temperature calculations
        if x12(b) > 1023                    % Safety shield to catch invalid data. A number higher than 1023 will cause R2 to go
            x12(b) = 1023;                  % negative which will give an error when the natural logarithm is applied to it.
        end                                 % This shield will make the number go to 0 so no error will occur but the invalid
% data will still be visible in the graph.
        R1 = 10000;                         % Calculations explained in the report.
        c1 = 1.129252142e-03;
        c2 = 2.341083183e-04;
        c3 = 0.8773267909e-07;
        R2 = R1.*(1023./x12(b)-1);
        logR2 = reallog(R2);
        temper = 1./(c1+c2.*logR2+c3.*logR2.*logR2.*logR2);
        x1(b) = temper-273.15;

        if x1(b) < 0                        % This makes sure that invalid data in the graph shows the value 0.
            x1(b) = 0;
        end
    end
    
    Temp = movmean(x1,101);                     % Because of noise in the temperature sensor, a moving mean is used to smoothen
% out peaks and valleys in the data.
    figure(1)                                   % Plotting the temperature of all 4 tests in 1 figure with it's maximum value
    subplot(length(z),1,r+1)                    
    plot(t1,Temp)
    title(['Temperature with max = ' num2str(max(Temp)) ' Test ' num2str(r+1)])
    xlabel('Time (s)')
    ylim([0 45])
    xlim([0 1200])
    ylabel('Temperature (C)')

%% Second section, plot the horizontal accelerometer (x2)

    pad=33554432-length(x2);                 % Zero padding to heigthen the quality of the FFT to a power of 2
    X=padarray(x2,pad,'post');              % All files are not the same length but this way it cancels errors
    L1=length(X);                           % Length of the padded signal = 2500000

    figure(2)                               % Plot the signal in the time domain
    subplot(length(z),1,r+1)
    plot(t1,x22)                          
    title(['Horizontal accelerometer output signal Test ' num2str(r+1)])       % Title of the signal with the test number
    xlabel('Time (s)')                      % The x-axile in time
    ylabel('Amplitude (V)')                 % The y-axile in volts
    ylim([-2 2])                            % Limits are used to make sure that invalid data points do not inter with the
    xlim([0 1200])                          % visibility of the graphs. This is the case for every figure.

    Y=fft(X);                               % Carrying out the Fast Fourier Transform

    P2 = abs(Y/L);                          % Absolute value of the FFT devided by the original signal length
    P1 = P2(1:L1/2+1);                      % Plots the figure from 0 to pi in the frequency domain
    P1(2:end-1) = 2*P1(2:end-1);            % Makes P1 to only plot the positive halve of the unity circle

    %Ydb=mag2db(P1);                        % Converts the values to decibel
    f = fs*(0:(L1/2))/L1;                   % To get the x-axile in frequency
    %k=(0:2:L)/L1;                          % To get the x-axile in Omega/pi
    
    figure(3)                               % Plots the results of the FFT in the frequency domain
    subplot(length(z),1,r+1)
    plot(f,P1)                         
    title(['FFT signal Horizontal accelerometer output Test ' num2str(r+1)])   % Titel FFT signal with the test number
    xlabel('Frequency (Hz)')                % x-axile in Frequency
    ylabel('Amplitude (V/Hz)')              % y-axile, Frequency's amplitude in V/Hz
    ylim([0 5e-3])                          % Limit to make sure that the peak at close to 0 Hz doesn't affect the graph too much

%% Third section, plot the Vertical accelerometer (x3)
% Includes the same codelines as the second section.

    pad=33554432-length(x3);                 
    X=padarray(x3,pad,'post');                      
    L1=length(X);                       

    figure(4)                           
    subplot(length(z),1,r+1)
    plot(t1,x32)                          
    title(['Vertical accelerometer output signal Test ' num2str(r+1)])      
    xlabel('Time (s)')                  
    ylabel('Amplitude (V)')
    ylim([-2 2])
    xlim([0 1200])

    Y=fft(X);                          

    P2 = abs(Y/L);                     
    P1 = P2(1:L1/2+1);                  
    P1(2:end-1) = 2*P1(2:end-1);        

    %Ydb=mag2db(P1);                     
    f = fs*(0:(L1/2))/L1;                
    %k=(0:2:L)/L1;                       
    
    figure(5)                          
    subplot(length(z),1,r+1)
    plot(f,P1)                        
    title(['FFT signal Vertical accelerometer output Test ' num2str(r+1)])   
    xlabel('Frequency (Hz)')          
    ylabel('Amplitude (V/Hz)')
    ylim([0 5e-3])

%% Fourth section, plot of the microphones (x4 ,x5 ,x6 ,x7(mean))
% Also includes the same codelines als section 2. New lines will be
% explained.

    x7 = mean([x4, x5, x6],2);              % Calculates the mean of the three other microphones in demension 2 -> rows    
    i = [4,5,6,7];                          % Creates an array of the 4 signals

    g4 = 'Microphone top-left';             % Assigning variables to the names of the microphones for the plotting
    g5 = 'Microphone top-right';            % in the for loop
    g6 = 'Microphone bottom';
    g7 = 'Microphone mean';

    for n = i                               % Nested for loop to do the analysis of all 4 microphone signals for all 4 tests
        signal = eval(sprintf('x%d',n));    % Assigns the variable 'signal' to signal x4 till x7.
        Titles = convertCharsToStrings(eval(sprintf('g%d',n)));   % Generates a fitting title string for the plotting called Titles
        pad=33554432-length(signal);                 
        X=padarray(signal,pad,'post');              
        L1=length(X);                       

        w=find(n==i);                       % To assign a position in the figure for the plot. Gives the position in the array where
% n is equal to i. This integer determains the position in the subplot
        figure(6)                           % Plotting the signals in the time domain.
        subplot(length(i),length(z),w+4*r)  % Subplot of 4 tests with 4 microphones is 4x4=16 plots. This line is the reason why the
% signals are from 0 to 3, to get the positions right (1+4*0 till 4+4*3)
        plot(t1,eval(sprintf('x%d2',n)))                          
        title('signal ' + Titles + [' Test ' num2str(r+1)])       % Title with microphone position (Titles) and test number (r+1)
        xlabel('Time (s)')                  
        ylabel('Amplitude (V)')             
        ylim([-2 2])
        xlim([0 1200])

        Y=fft(X);                           

        P2 = abs(Y/L);                      
        P1 = P2(1:L1/2+1);                  
        P1(2:end-1) = 2*P1(2:end-1);        

        %Ydb=mag2db(P1);                    
        f = fs*(0:(L1/2))/L1;               
        %k=(0:2:L)/L1;                      
    
        figure(7)                           % Plots the results of the FFT's in the frequency domain
        subplot(length(i),length(z),w+4*r)  % Same amount of subplots and counting system as Figure(6)
        plot(f,P1)                        
        title('FFT signal ' + Titles + [' Test ' num2str(r+1)])   % FFT Title with microphone position (Titles) + test number (r+1)
        xlabel('Frequency (Hz)')            
        ylabel('Amplitude (V/Hz)')          
        ylim([0 5e-3])
    end
end


