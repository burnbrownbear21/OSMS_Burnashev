a = [0.3 0.2 -0.1 4.2 -2 1.5 0];
b = [0.3 4 -2.2 1.6 0.1 0.1 0.2];

figure;
subplot(4,1,1);
plot(a);
title('Массив a');
subplot(4,1,2);
plot(b);
title('Массив b');

% Вычисление взаимной корреляции
corr = zeros(1,length(b)); 
for i=1:length(b)
    b_shift = [zeros(1,i-1) b(1:end-i+1)];
    corr(i) = sum(a.*b_shift);
end
% Построение зависимости взаимной корреляции от величины сдвига
corr_1 = [0 corr(1:end-1)];
subplot(4,1,3:4);
plot(corr_1);
title('Зависимость взаимной корреляции от величины сдвига');

% Определение максимальной корреляции и соответствующего сдвига
[max_corr, max_index] = max(corr);
shift = max_index - 1;

% Сдвиг массива b на величину максимальной корреляции
b_shifted = [zeros(1,shift) b(1:end-shift)];

figure;
subplot(2,1,1);
plot(a);
title('Массив a');
subplot(2,1,2);
plot(b_shifted);
title('Массив b, сдвинутый на максимальную корреляцию');

