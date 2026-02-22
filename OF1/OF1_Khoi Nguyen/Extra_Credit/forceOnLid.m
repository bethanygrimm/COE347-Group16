clear; clc; close all;

U  = 1.0;      
L  = 0.1;      

out_10 = lidShearFromCSVs(".\csv_out\160_10_AR.5_lid_U.csv", ".\csv_out\160_10_AR.5_below_lid_U.csv", 0.01, U, L);
out_100 = lidShearFromCSVs(".\csv_out\160_100_AR.5_lid_U.csv", ".\csv_out\160_100_AR.5_below_lid_U.csv", 0.001, U, L);
out_250 = lidShearFromCSVs(".\csv_out\160_250_AR.5_lid_U.csv", ".\csv_out\160_250_AR.5_below_lid_U.csv", 0.0004, U, L);
out_500 = lidShearFromCSVs(".\csv_out\160_500_AR.5_lid_U.csv", ".\csv_out\160_500_AR.5_below_lid_U.csv", 0.0002, U, L);

out_10_AR2 = lidShearFromCSVs(".\csv_out\160_10_AR2_lid_U.csv", ".\csv_out\160_10_AR2_below_lid_U.csv", 0.01, U, L);
out_100_AR2 = lidShearFromCSVs(".\csv_out\160_100_AR2_lid_U.csv", ".\csv_out\160_100_AR2_below_lid_U.csv", 0.001, U, L);
out_250_AR2 = lidShearFromCSVs(".\csv_out\160_250_AR2_lid_U.csv", ".\csv_out\160_250_AR2_below_lid_U.csv", 0.0004, U, L);
out_500_AR2 = lidShearFromCSVs(".\csv_out\160_500_AR2_lid_U.csv", ".\csv_out\160_500_AR2_below_lid_U.csv", 0.0002, U, L);

F_tilde_Ctrl = [15.0027   16.1273   18.8857   22.4815];
F_tilde = [out_10.F_tilde out_100.F_tilde out_250.F_tilde out_500.F_tilde];
F_tilde_AR2 = [out_10_AR2.F_tilde out_100_AR2.F_tilde out_250_AR2.F_tilde out_500_AR2.F_tilde];
Re = [10 100 250 500];
figure;
hold on;
plot(Re, F_tilde_Ctrl,'Marker','+', 'LineWidth',1.5, 'Color', 'k');
plot(Re, F_tilde,'Marker','x', 'LineWidth',1.5, 'Color', 'b'); 
plot(Re, F_tilde_AR2,'Marker','o', 'LineWidth',1.5, 'Color', 'r');
grid on;
xlabel('Re', 'FontSize',14);
ylabel('$\tilde{F}$', 'Interpreter','latex', 'FontSize',14);
title('Lid Nondimensional Force $\tilde{F}$ vs $Re$', 'Interpreter','latex', 'FontSize',14);
legend({'AR=1','AR=0.5','AR=2'},'Location','southeast');
ylim([14.5 23]);

function out = lidShearFromCSVs(lidCsv, belowCsv, mu, U, L)
    Tlid   = readtable(lidCsv);
    Tbelow = readtable(belowCsv);
    Tlid   = sortrows(Tlid,   'x');
    Tbelow = sortrows(Tbelow, 'x');
    x_lid   = Tlid.x;

    y_lid   = mean(Tlid.y);
    y_below = mean(Tbelow.y);
    dy = y_lid - y_below;
    Ux_lid = Tlid.U_x;
    Ux_below_on_lid = Tbelow.U_x;

    du_dy_lid = (Ux_lid - Ux_below_on_lid) / dy;
    tau = mu * du_dy_lid;          
    F   = trapz(x_lid, tau);       

    x0 = min(x_lid);

    x_tilde   = (x_lid - x0) / L;
    tau_tilde = tau * (L/(mu*U));  
    F_tilde   = F / (mu*U);

    out.x         = x_lid;
    out.dy        = dy;
    out.du_dy_lid = du_dy_lid;
    out.tau       = tau;
    out.F         = F;
    out.x_tilde   = x_tilde;
    out.tau_tilde = tau_tilde;
    out.F_tilde   = F_tilde;
    out.L         = L;

    % figure;
    % plot(out.x_tilde, out.tau_tilde, 'LineWidth', 1.5);
    % grid on;
    % xlabel('$\tilde{x}$', 'Interpreter','latex', 'FontSize',14);
    % ylabel('$\tilde{\tau} = \tau L / (\mu U)$', 'Interpreter','latex', 'FontSize',14);
    % title(sprintf(['Lid nondimensional shear stress ', '($\\tilde{F}=%.4f$, $\\Delta y=%.6g$)'], out.F_tilde, out.dy), 'Interpreter','latex', 'FontSize',14);
    % ylim([0 75]);
end
