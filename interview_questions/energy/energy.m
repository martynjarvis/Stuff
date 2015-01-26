cd C:\Users\Martyn\Projects\energy-usage
M = csvread('energy_data_combined SW.csv');
ts =timeseries(M(:,2),M(:,1));

% % look at time resolution over data
% plot(ts.Time/(60*60*24), [diff(ts.Time); 1])
% xlabel('Time (Days)')
% ylabel('Time Resolution of data (s)')

% resample to constant time resolution
res_ts=resample(ts,min(M(:,1)):60:max(M(:,1)));
ref_time = datenum('2010-12-16T12:17:32','yyyy-mm-ddTHH:MM:SS');

% offest first day, discard incomplete days
newday = datenum('2010-12-17','yyyy-mm-dd');
mask = res_ts.Time > newday;
data = res_ts.Data(mask);
nDays = floor(numel(data)/(24*60));

% dif to get power usage, 
% divide by 60 to go from Watt seconds to Watt
% multiply by 256 because of units (see instructions)
data = diff(data(1:(nDays*24*60+1))).*(256/60);

% reshape in to row=minsofday col=days
data = reshape(data,60*24,896);

% % produce average consumption
avgUsage = mean(data,2);
hours = 0:1.0/60.0:23.9834; % hours as x axis rather than seconds
plot(hours,avgUsage)
xlabel('Time of day (Hours)')
ylabel('Average power usage (W)')

% day by day usage
dayUsage = sum(data*(60/3600)*(1/1000),1); % convert from  Ws to KWh
day = 1:nDays;
[ft,ErrorEst] = polyfit(day,dayUsage,8); 
ftdat = polyval(ft,day',ErrorEst);
plot(day',ftdat,'--',day',dayUsage,'-')
xlabel('Time since 2010-12-16  (Days)')
ylabel('Energy usage (kW.h)')

% background model (something that's always on, fridge?) 
% (day 627 on holiday)
[bkg,ErrorEst] = polyfit(hours',data(:,627),0); % just a horizontal line is fine
bkgFit = polyval(bkg,hours',ErrorEst);
 
j = 825; % example day to look at
plot(hours',bkgFit,'--',hours',data(:,j),'-');
xlabel('Time of day (Hours)')
ylabel('Power usage (W)')
hleg1 = legend('Constant background','Power usage');

% devices turning on and off (day)
powerRate = [diff(data(:,j))/60; 0];

plot(hours',powerRate);
xlabel('Time of day (Hours)')
ylabel('Change in power usage (W/s)')

% % plot histogram of devices turning on and off over a certain threshold
% powerRate = (data(:,j:j+30))/60;
% reshape(powerRate.',[],1)
% powerRate = diff(powerRate);
% threshold = 5;
% mask = powerRate > threshold | powerRate < -threshold;
% hist(powerRate(mask),-50:50)

