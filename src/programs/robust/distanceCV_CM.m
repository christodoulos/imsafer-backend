function e=distanceCV_CM(x, plate)
CMx = plate.CMx; % ΚΕΝΤΡΟ ΜΑΖΑΣ ΤΗΣ ΚΑΤΟΨΗΣ ΩΣ ΠΡΟΣ ΤΟ ΕΠΙΛΕΓΕΝ ΣΥΣΤΗΜΑ ΑΝΑΦΟΡΑΣ (παραδοχή ομοιόμορφου κατανεμημένου φορτίου στις πλάκες)
CMy = plate.CMy; % ΚΕΝΤΡΟ ΜΑΖΑΣ ΤΗΣ ΚΑΤΟΨΗΣ ΩΣ ΠΡΟΣ ΤΟ ΕΠΙΛΕΓΕΝ ΣΥΣΤΗΜΑ ΑΝΑΦΟΡΑΣ (παραδοχή ομοιόμορφου κατανεμημένου φορτίου στις πλάκες)
Data = plate.Data;

hl=0.01; % πάχος λωρίδας
V=zeros(size(Data,1),2) ;
e=zeros(size(x,1),1);

for sx=1:size(x,1) % για κάθε χώρα/σχεδιασμό υπολογισμός του e
for i=1:size(Data,1) % πλήθος υποστυλωμάτων
 % στις στήλες 2i-1 του πίνακα x βρίσκονται οι θέσεις των τιμών των παχών
 % ενίσχυσης στο πίνακα του πεδίου τιμών τους
    if Data(i,7)== 0 && x(sx,2*i-1)~=1
        Data(i,9)=0.08 + (x(sx,2*i-1)-2)*0.01; % μη ενισχυμένα αρχικώς υποστυλώματα
    elseif Data(i,7)~=0 && x(sx,2*i-1)~=1
        Data(i,9)=0.01 + (x(sx,2*i-1)-2)*0.01;  % ενισχυμένα αρχικώς υποστυλώματα
    else
        Data(i,9)=0;
    end
    % τα γεωμετρικά ποσοστά του οπλισμού ενίσχυσης βρίσκονται στις στήλες
    % 2i του πίνακα x
    Data(i,10)=x(sx,2*i) ;

    Asarx = Data(i,1)*Data(i,2)*Data(i,3)      ;     % συνολικός οπλισμός ενίσχυσης αρχικής-μη ενισχυμένης διατομής
    Aso = Data(i,8)*(2*(Data(i,1)+Data(i,2))*Data(i,7)+4*Data(i,7)^2) ;    % συνολικός οπλισμός ενίσχυσης που προέκυψε από απαιτήσεις αντοχής του στοιχείου
    Asnew = Data(i,10)*(2*(Data(i,1)+Data(i,2))*Data(i,9)+4*Data(i,9)^2) ;    % συνολικός οπλισμός ενίσχυσης που προκύπτει από ανάγκες βελτιστοποίησης της δυστρεψίας
    Astot = Aso + Asnew ;         % συνολικός οπλισμός ενίσχυσης
    t_tot = Data(i,7) + Data(i,9)     ;   % συνολικό πάχος ενίσχυσης

    l= round([(Data(i,1)+2*t_tot)/hl ; (Data(i,2)+2*t_tot)/hl ]) ;  % l(1,1) διακριτές λωρίδες // y, l(2,1) διακριτές λωρίδες // x
for d =1:2   % υπολογισμός τέμνουσας αντοχής σε κάθε διεύθυνση d=1-->y (My, Vx) και d=2-->x (Mx, Vy)
    htot = Data(i,d) + 2*t_tot ;   % γεωμετρικό ύψος διατομής
    ec=zeros(l(d,1),1) ;
    es=zeros(4,1)  ;
    % θεωρείται θετική η θλίψη και αρνητικός ο εφελκυσμός
    % ελέγχουμε αν έχουμε αστοχία του χάλυβα (εντατική περιοχή 2) ή της
    % θλιβόμενης ζώνης του σκυροδέματος (εντατ. περιοχές 3,4,5)
    ecc = 0.0035  ;
    es1 = -0.0675   ;
    hc = ecc/(ecc-es1)*(htot-0.04)   ;   % ύψος θλιβόμενης ζώνης

    % υπολογισμός παραμορφώσεων άνω ινών λωρίδων
    for j=0:(l(d,1)-1)
        s=hl*j  ;  % απόσταση άνω ορίου λωρίδας από την πλέον θλιβόμενη ίνα
        ec(j+1,1)= (hc-s)/hc*ecc   ; % θετικές παραμορφώσεις θλιπτικές δυνάμεις, αρνητικές παραμορφώσεις εφελκυστικές δυνάμεις
    end

    % υπολογισμός παραμορφώσεων οπλισμών
    St_opl = [htot-0.04; htot-t_tot-0.04; t_tot+0.04; 0.04]   ;   % στάθμες οπλισμών μετρούμενες από την πλέον θλιβόμενη ίνα - κάνουμε παραδοχή επικάλυψης οπλισμών 3cm και Φ20mm
    for j=1:4
    es(j,1) = (hc-St_opl(j,1))/hc*ecc ; % θετικές παραμορφώσεις θλιπτικές δυνάμεις, αρνητικές παραμορφώσεις εφελκυστικές δυνάμεις
    end

    [Fc,m,Fctot]=dynameis_mohlovrah_skyrod(ec,l,d,Data,i,htot,hl);
    [Fs,Fstot]=dynameis_oplism(es,Astot,Asarx);
    a=(Fstot+Fctot-Data(i,14))/Data(i,14)      ;                            % Data(i,14) η αξονική θλίψη N του υποστυλώματος i

    if abs(a)<= 0.02                                                       % θεωρείται ικανοποιητικό ένα σφάλμα μέχρι 2%
        M=ropi_antohis(Fc,m,Fs,htot,l,d,t_tot)  ;
    elseif Data(i,14)<Fctot+Fstot
        % ανάγκη μείωσης θλιβόμενης ζώνης --> εντατική περιοχή 2 es1=-0.0675
        b=0:0.0001:0.0035 ;    % παραμορφώσεις σκυροδέματος με ακρίβεια 4ου δεκαδικού ψηφίου
        for j=1:size(b,2)
            ecc=b(1,j)   ;
            hc=ecc/(ecc+0.0675)*(htot-0.04)  ;
            for k=0:(l(d,1)-1)
                s=hl*k   ;
                ec(k+1,1)=(hc-s)/hc*ecc ;
            end
            for k=1:4
                es(k,1) = (hc-St_opl(k,1))/hc*ecc ;
            end
            [Fc,m,Fctot]=dynameis_mohlovrah_skyrod(ec,l,d,Data,i,htot,hl);
            [Fs,Fstot]=dynameis_oplism(es,Astot,Asarx);
            a=(Fstot+Fctot-Data(i,14))/Data(i,14)      ;
            if abs(a)<=0.02
                 M=ropi_antohis(Fc,m,Fs,htot,l,d,t_tot)  ;
                 break
            end
        end
    else
        % αστοχία θλιβόμενης ζώνης σκυροδέματος
        ecc=0.0035  ;  % & ec1=0 : όριο εντατικών περιοχών (3,4,4α) & 5
        hc=htot ;
        for j=0:(l(d,1)-1)
            s=hl*j ;
            ec(j+1,1)= (hc-s)/hc*ecc   ;
        end
        for j=1:4
            es(j,1) = (hc-St_opl(j,1))/hc*ecc ;
        end

        [Fc,m,Fctot]=dynameis_mohlovrah_skyrod(ec,l,d,Data,i,htot,hl);
        [Fs,Fstot]=dynameis_oplism(es,Astot,Asarx);
        a=(Fstot+Fctot-Data(i,14))/Data(i,14)      ;

        if abs(a)<= 0.02
             M=ropi_antohis(Fc,m,Fs,htot,l,d,t_tot)  ;
        elseif Data(i,14)<Fctot+Fstot
            %ανάγκη μείωσης θλιβόμενης ζώνης --> εντατικές περιοχές 3,4,4α
            ecc=0.0035 ;
            b=-0.0675:0.0001:0.04*ecc/htot ;
            for j=1:size(b,2)
                es(1,1)=b(1,j) ;
                hc=ecc*(htot-0.04)/(ecc-es(1,1)) ;
                 for k=0:(l(d,1)-1)
                     s=hl*k   ;
                     ec(k+1,1)=(hc-s)/hc*ecc ;
                 end
                 for k=2:4
                     es(k,1) = (hc-St_opl(k,1))/hc*ecc ;
                 end
                [Fc,m,Fctot]=dynameis_mohlovrah_skyrod(ec,l,d,Data,i,htot,hl);
                [Fs,Fstot]=dynameis_oplism(es,Astot,Asarx);
                a=(Fstot+Fctot-Data(i,14))/Data(i,14)      ;
                if abs(a)<=0.02
                    M=ropi_antohis(Fc,m,Fs,htot,l,d,t_tot) ;
                    break
                end
            end
        else
            % ανάγκη αύξησης θλιβόμενης ζώνης --> εντατική περιοχή 5
            b=0.0021:0.0001:0.0035;                   % ξεκινάμε με παραμόρφωση 0,0021 αντί για 0,0020 γιατί διαφορετικά θα απειριζόταν το hc και γιατί αποκλείεται η διατομή να μην έχει ροπή και να έχουμε κεντρική θλίψη
            for j=1:size(b,2)
                ecc=b(1,j)  ;
                hc=3/7*ecc*htot/(ecc-0.002) ;
                for k=0:(l(d,1)-1)
                    s=hl*k   ;
                    ec(k+1,1)=(hc-s)/hc*ecc ;
                end
                for k=1:4
                    es(k,1) = (hc-St_opl(k,1))/hc*ecc ;
                end
                [Fc,m,Fctot]=dynameis_mohlovrah_skyrod(ec,l,d,Data,i,htot,hl);
                [Fs,Fstot]=dynameis_oplism(es,Astot,Asarx);
                a=(Fstot+Fctot-Data(i,14))/Data(i,14)      ;
               if abs(a)<=0.02
                   M=ropi_antohis(Fc,m,Fs,htot,l,d,t_tot)  ;
                   break
               end
            end
        end
    end
    if Data(i,7)~=0 || Data(i,9)~=0   %εξασφάλιση ύπαρξης μανδύα
        V(i,d)=0.9*M/(0.5*Data(i,13)) ;  % 0.9: συντελ. απομείωσης αντοχής λόγω θεώρησης μονολιθικότητας (ΚΑΝΕΠΕ)
    else
        V(i,d)= M/(0.5*Data(i,13)) ;   % μη ενισχυμένη με μανδύα διατομή
    end
end
end
SVxY=0 ;
SVyX=0 ;
SVx=0 ;
SVy=0 ;
for i=1:size(Data,1)
    SVxY=SVxY+V(i,1)*Data(i,5) ;
    SVyX=SVyX+V(i,2)*Data(i,4) ;
    SVx=SVx+V(i,1) ;
    SVy=SVy+V(i,2) ;
end

% υπολογισμός συντεταγμένων CV
CVx=SVyX/SVy ;
CVy=SVxY/SVx ;

% υπολογισμός εκκεντρότητας CV - CM
ex=CMx-CVx;
ey=CMy-CVy;
e(sx,1)=sqrt(ex^2+ey^2); % κάθε γραμμή του πίνακα αναφέρεται σε διαφορετικό σχεδιασμό/χώρα
findxmin(e, x, sx); %Thanasis2021_12_25
end
end


function [Fs,Fstot]=dynameis_oplism(es,Astot,Asarx)
    % ΕΔΩ ΔΗΛΩΝΟΥΜΕ ΤΙΣ ΙΔΙΟΤΗΤΕΣ ΤΟΥ ΧΑΛΥΒΑ ΤΩΝ ΜΑΝΔΥΩΝ
    fyk_man = 500;  % se Mpa
    Es_man =200000 ;   % se Mpa
    % ΕΔΩ ΔΗΛΩΝΟΥΜΕ ΤΙΣ ΙΔΙΟΤΗΤΕΣ ΤΟΥ ΧΑΛΥΒΑ ΤΗΣ ΜΗ ΕΝΙΣΧΥΜΕΝΗΣ ΔΙΑΤΟΜΗΣ
    fyk_arx = 500;   % se Mpa
    Es_arx = 200000;  % se Mpa

    fyd_man = 1.05*fyk_man/1.15   ;
    eyd_man = fyd_man/Es_man ;

    fyd_arx = fyk_arx/1.10 ;
    eyd_arx = fyd_arx/Es_arx ;

    As=1/4*[Astot;Asarx;Asarx;Astot] ; % θεωρούμε ομοιόμορφη κατανομή των οπλισμών στις 4 πλευρές
    eyd=[eyd_man;eyd_arx;eyd_arx;eyd_man]  ;
    Es=[Es_man;Es_arx;Es_arx;Es_man]  ;
    fyd=[fyd_man;fyd_arx;fyd_arx;fyd_man]  ;

    Fstot=0  ;
    Fs=zeros(4,1) ;
    for q=1:4
        if abs(es(q,1))>=eyd(q,1)
            Fs(q,1)=sign(es(q,1))*fyd(q,1)*As(q,1)*10^3 ; % se kN
        else
            Fs(q,1)=es(q,1)*Es(q,1)*As(q,1)*10^3  ; % se kN
        end
        Fstot=Fstot+Fs(q,1)  ;
    end
end


function [Fc,m,Fctot]=dynameis_mohlovrah_skyrod(ec,l,d,Data,i,htot,hl)
    fck_man = 20 ; % edw dhlwnoume thn charaktiristiki timh toy skyrodematos enisxyshs (�Pa)
    fck_arx = 20 ; % edw dhlwnoume thn charaktiristiki timh toy skyrodematos thw MH enisxymenhs diatomis (�Pa)

    fcd_man = min(1.2*fck_man,fck_man+5)/1.15 ;  % antoxi skyrodematos enisxymenhs diatomis
    fcd_arx = (fck_arx+8)/1.10 ;  % antoxi skyrodematos MH enisxymenhs diatomis

    Fctot=0;
    Fc=zeros(l(d,1),1) ;
    m=zeros(l(d,1),1) ;
    for o=0:(l(d,1)-1)
        % elegxoume an exoume enisxymeni h mh diatomh gia na xrisimopoiisoume analogi antoxi skyrodematos
        if Data(i,7)~=0 || Data(i,9)~=0        % enisxymenh diatomi
            if ec(o+1,1)>=0 && ec(o+1,1)<=0.002
                tasi=1000*ec(o+1,1)*(1-250*ec(o+1,1))*fcd_man ; % apo ypologistiko diagramma tasewn-paramorfosewn skyrodematos se thlipsi, theorontas thetiki thn thlipsi
            elseif ec(o+1,1)>0.002
                tasi=fcd_man ;
            else
                tasi=0 ;
            end
        else % MH enisxymenh diatomi
             if ec(o+1,1)>=0 && ec(o+1,1)<=0.002
                 tasi=1000*ec(o+1,1)*(1-250*ec(o+1,1))*fcd_arx ;
             elseif ec(o+1,1)>0.002
                 tasi=fcd_arx ;
             else
                 tasi=0 ;
             end
        end
         s=hl*o ;
        % ypologismos dynamewn lwridwn 
        if d==1 % // dieythinsi y
            Fc(o+1,1)=tasi*(Data(i,2)+2*(Data(i,7)+Data(i,9)))*hl*10^3  ;  % se kN
        else % // dieythinsi x
            Fc(o+1,1)=tasi*(Data(i,1)+2*(Data(i,7)+Data(i,9)))*hl*10^3 ;  % se kN
        end
        Fctot=Fctot+Fc(o+1,1) ;
        % ypologismos moxlobraxionwn lwridwn
        m(o+1,1)=htot/2-(s+hl/2) ; % ws pros to K.B. thw lwridas (s+0.01) - se lwrides katw skyrodematos panw apo th K.B.G. m>0 --> M>0 enw katw apo thn K.B.G. m<0 --> M<0
    end
end


function M=ropi_antohis(Fc,m,Fs,htot,l,d,t_tot)
    Fcm=0;
    for q=1:l(d,1)
        Fcm=Fc(q,1)*m(q,1)+Fcm ;
    end
    M=Fcm+(Fs(4,1)-Fs(1,1))*(htot/2-0.04)+(Fs(3,1)-Fs(2,1))*(htot/2-t_tot-0.04) ;
end


function findxmin(e, x, sx)  %Thanasis2021_12_25
    %Save minimum e and correspondin x.
    global eplate
    if isempty(eplate) || e(sx, 1) < eplate.emin   %Thanasis2021_12_25
        eplate.emin = e(sx, 1);
        eplate.xmin = x(sx, :);
    end
end
