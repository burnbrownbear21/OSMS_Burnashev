f1 = 8;
f2 = 8 + 4;
f3 = 8 * 2 + 1;
t = [0:100-1]/100;
s1 = cos(2*pi*f1*t);
s2 = cos(2*pi*f2*t);
s3 = cos(2*pi*f3*t);
a = 2*s1 + 4*s2 + s3;
b = s1 + s2;
% формула 3.2
corr_ab = sum(a.*b);
corr_ac = sum(a.*s1);
corr_bc = sum(b.*s2);
% формула 3.3
corr_ab_norm = corr_ab / sqrt((sum(a.^2)) * (sum(b.^2)));
corr_ac_norm = corr_ac / sqrt((sum(a.^2)) * (sum(s1.^2)));
corr_bc_norm = corr_bc / sqrt((sum(b.^2)) * (sum(s2.^2)));

fprintf('Корреляция между a и b: %f\n', corr_ab);
fprintf('Корреляция между a и s1: %f\n', corr_ac);
fprintf('Корреляция между b и s2: %f\n', corr_bc);
fprintf('Нормализованная корреляция между a и b: %f\n', corr_ab_norm);
fprintf('Нормализованная корреляция между a и s1: %f\n', corr_ac_norm);
fprintf('Нормализованная корреляция между b и s2: %f\n', corr_bc_norm);
