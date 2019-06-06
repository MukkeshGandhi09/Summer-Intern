clear all;
close all;

%Gyroscope measurement correction
rolltruek1=0.0;
rolltruek=0.0;
rollveltrue=0.0;
gyrosigmanoise=0.002;
accsignmanoise=sqrt(0.03);
gyrodrifttrue=1.0;
gyrobiastrue=0.01;

accelmeask1=0.0;
accelmeask=0.0;
gyromeask1=0.0;
gyromeask=0.0;

delt=0.004;
time=0;
datastore=zeros(5010,7);

rollanglek1=0.0;
rollanglek=0.0;

gaink1=0.98;
gaink2=0.02;

%Kalman filter gains
xk=zeros(1,2);
pk=[0.5 0 0 0.01];
k=zeros(1,2);
phi=[1 delt 0 1];
psi=[delt 0];

endpoint=2500;

for i=1:endpoint;
    rollveltrue=0.0;
    if (i>=500) && (i<=750);
        rollveltrue=30.0;
    end
    if (i>=1250) && (i<=1500);
        rollveltrue=-40.0;
    end
    if (i>=1750) && (i<=2000);
        rollveltrue=10.0;
    end
rolltruek1=rolltruek+rollveltrue*delt;
accelmeask1=rolltruek1+randn(1)+accsigmanoise;

gyroread1=rollveltrue-gyrodrifttrue+randn(1)* gyrosigmanoise+gyrobiastrue;
gyromeask1=gyroreadk1-gyrobiastrue;

anglerollk1=gaink2*accmeask1+gaink1*(anglerollk+gyromeask1*delt);

uk=gyromeask1;
zk=accelmeask1;

xk1minus(1)=phi(1)*xk1(1)+phi(2)+xk1(2)+psi(1)*uk;
xk1minus(2)=phi(3)*xk1(1)+phi(4)+xk1(2)+psi(2)*uk;

pk1minus(1)=(phi(1)*pk(1)+phi(2)*pk(3))*phi(1)