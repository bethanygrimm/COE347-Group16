clear; clc; close all;

U  = 1.0;      
L  = 0.1;      

out_10 = lidShearFromCSVs("160_10_lid_U.csv", "160_10_below_lid_U.csv", 0.01, U, L);
out_100 = lidShearFromCSVs("160_100_lid_U.csv", "160_100_below_lid_U.csv", 0.001, U, L);
out_250 = lidShearFromCSVs("160_250_lid_U.csv", "160_250_below_lid_U.csv", 0.0004, U, L);
out_500 = lidShearFromCSVs("160_500_lid_U.csv", "160_500_below_lid_U.csv", 0.0002, U, L);

F_tilde = [out_10.F_tilde out_100.F_tilde out_250.F_tilde out_500.F_tilde];
Re = [10 100 250 500];
figure;
plot(Re, F_tilde,'Marker','o', 'LineWidth',1.5);
grid on;
xlabel('Re', 'FontSize',14);
ylabel('$\tilde{F}$', 'Interpreter','latex', 'FontSize',14);
title('Lid Nondimensional Force $\tilde{F}$ vs $Re$', 'Interpreter','latex', 'FontSize',14);
ylim([0 25]);

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

    figure;
    plot(out.x_tilde, out.tau_tilde, 'LineWidth', 1.5);
    grid on;
    xlabel('$\tilde{x}$', 'Interpreter','latex', 'FontSize',14);
    ylabel('$\tilde{\tau} = \tau L / (\mu U)$', 'Interpreter','latex', 'FontSize',14);
    title(sprintf(['Lid nondimensional shear stress ', '($\\tilde{F}=%.4f$, $\\Delta y=%.6g$)'], out.F_tilde, out.dy), 'Interpreter','latex', 'FontSize',14);
    ylim([0 75]);
end
