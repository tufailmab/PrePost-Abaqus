# GetResults.py Flowchart

This flowchart illustrates the complete workflow of the GetResults.py (V2) script. The script scans the working directory for Abaqus .odb files, extracts the required simulation results from each database, and records the maximum values for stress, creep strain, plastic strain, equivalent plastic strain (PEEQ), and displacement for every model instance. The extracted data from all processed files is consolidated into a single Results.csv file inside the All Required Outputs directory. Error handling is included to ensure that invalid or inaccessible files do not interrupt the overall processing workflow. The diagram below provides a step-by-step overview of the script's execution, from initialization through data extraction to final CSV generation.

flowchart TD
    %% Style Definitions
    classDef startEnd fill:#2E86C1,stroke:#1B4F72,stroke-width:3px,color:#FFFFFF,font-weight:bold,font-size:14px
    classDef process fill:#28B463,stroke:#1E8449,stroke-width:2px,color:#FFFFFF,font-weight:bold
    classDef decision fill:#F39C12,stroke:#D68910,stroke-width:2px,color:#FFFFFF,font-weight:bold
    classDef io fill:#8E44AD,stroke:#6C3483,stroke-width:2px,color:#FFFFFF,font-weight:bold
    classDef file fill:#E74C3C,stroke:#B03A2E,stroke-width:2px,color:#FFFFFF,font-weight:bold
    classDef subprocess fill:#3498DB,stroke:#1F618D,stroke-width:2px,color:#FFFFFF
    classDef warning fill:#E67E22,stroke:#CA6F1E,stroke-width:2px,color:#FFFFFF
    classDef success fill:#2ECC71,stroke:#1D8348,stroke-width:2px,color:#FFFFFF
    classDef loop fill:#5D6D7E,stroke:#2C3E50,stroke-width:2px,color:#FFFFFF
    classDef error fill:#E74C3C,stroke:#922B21,stroke-width:3px,color:#FFFFFF,font-weight:bold
    classDef database fill:#A569BD,stroke:#7D3C98,stroke-width:2px,color:#FFFFFF
    classDef function fill:#48C9B0,stroke:#1ABC9C,stroke-width:2px,color:#FFFFFF

    %% Main Execution Flow
    A[Script Initialization Start] --> B[Import Required Modules]
    B --> C[Get Current Working Directory]
    C --> D[Validate Directory Path]
    D --> E{Directory Accessible}
    
    E -->|Access Denied| F[Log Error and Exit]
    E -->|Accessible| G[Create Output Directory Structure]
    
    G --> H{Output Folder Exists}
    H -->|Exists| I[Use Existing Output Folder]
    H -->|Not Exists| J[Create New Output Folder]
    
    I --> K[Define CSV Output File Path]
    J --> K
    
    K --> L[Initialize Results Data Structure]
    L --> M[Define Headers Row]
    M --> N[Define New Record Function]
    N --> O[Initialize Results List with Headers]

    O --> P[Start File Processing Loop]
    P --> Q[Get Next File in Directory]
    Q --> R{File Extension Check}
    
    R -->|Not ODB| Q
    R -->|Is ODB| S[Increment File Counter]
    
    S --> T[Display Processing Status]
    T --> U[Attempt to Open ODB File]
    U --> V{Open Successful}
    
    V -->|Error| W[Log Error and Continue]
    V -->|Success| X[Initialize Instance Results Dictionary]
    
    W --> P
    X --> Y[Start Step Iteration]
    Y --> Z[Get Next Step in ODB]
    Z --> AA{More Steps}
    
    AA -->|Yes| AB[Start Frame Iteration]
    AA -->|No| AC[Close ODB File]
    
    AB --> AD[Get Next Frame in Step]
    AD --> AE{More Frames}
    
    AE -->|Yes| AF[Initialize Field Processing]
    AE -->|No| Y
    
    AF --> AG[Process Stress Field S]
    AF --> AH[Process Creep Field CE]
    AF --> AI[Process Plastic Field PE]
    AF --> AJ[Process PEEQ Field]
    AF --> AK[Process Displacement Field U]

    %% Stress Processing Subgraph
    subgraph StressProcessing[Stress Field Processing]
        AG --> AL{Field S Exists}
        AL -->|No| AM[Skip Stress Processing]
        AL -->|Yes| AN[Extract Stress Values]
        AN --> AO[Iterate Through Values]
        AO --> AP{Instance Exists}
        AP -->|No| AQ[Create Instance Record]
        AP -->|Yes| AR[Retrieve Instance Record]
        AQ --> AS[Initialize Stress Fields]
        AR --> AT[Process S Component]
        AS --> AT
        AT --> AU[Update Mises Stress]
        AT --> AV[Update Max Principal]
        AT --> AW[Update S11 Component]
        AT --> AX[Update S22 Component]
        AT --> AY[Update S33 Component]
        AU --> AZ[Continue Next Value]
        AV --> AZ
        AW --> AZ
        AX --> AZ
        AY --> AZ
        AM --> BA[Stress Processing Complete]
        AZ --> BA
    end

    %% Creep Strain Processing Subgraph
    subgraph CreepProcessing[Creep Strain Processing]
        AH --> BB{Field CE Exists}
        BB -->|No| BC[Skip Creep Processing]
        BB -->|Yes| BD[Extract Creep Values]
        BD --> BE[Iterate Through Values]
        BE --> BF{Instance Exists}
        BF -->|No| BG[Create Instance Record]
        BF -->|Yes| BH[Retrieve Instance Record]
        BG --> BI[Initialize Creep Fields]
        BH --> BJ[Process CE Component]
        BI --> BJ
        BJ --> BK[Update Max Principal]
        BJ --> BL[Update CE11 Component]
        BJ --> BM[Update CE22 Component]
        BJ --> BN[Update CE33 Component]
        BK --> BO[Continue Next Value]
        BL --> BO
        BM --> BO
        BN --> BO
        BC --> BP[Creep Processing Complete]
        BO --> BP
    end

    %% Plastic Strain Processing Subgraph
    subgraph PlasticProcessing[Plastic Strain Processing]
        AI --> BQ{Field PE Exists}
        BQ -->|No| BR[Skip Plastic Processing]
        BQ -->|Yes| BS[Extract Plastic Values]
        BS --> BT[Iterate Through Values]
        BT --> BU{Instance Exists}
        BU -->|No| BV[Create Instance Record]
        BU -->|Yes| BW[Retrieve Instance Record]
        BV --> BX[Initialize Plastic Fields]
        BW --> BY[Process PE Component]
        BX --> BY
        BY --> BZ[Update Max Principal]
        BY --> CA[Update PE11 Component]
        BY --> CB[Update PE22 Component]
        BY --> CC[Update PE33 Component]
        BZ --> CD[Continue Next Value]
        CA --> CD
        CB --> CD
        CC --> CD
        BR --> CE[Plastic Processing Complete]
        CD --> CE
    end

    %% PEEQ Processing Subgraph
    subgraph PEEQProcessing[PEEQ Processing]
        AJ --> CF{Field PEEQ Exists}
        CF -->|No| CG[Skip PEEQ Processing]
        CF -->|Yes| CH[Extract PEEQ Values]
        CH --> CI[Iterate Through Values]
        CI --> CJ{Instance Exists}
        CJ -->|No| CK[Create Instance Record]
        CJ -->|Yes| CL[Retrieve Instance Record]
        CK --> CM[Initialize PEEQ Field]
        CL --> CN[Process PEEQ Component]
        CM --> CN
        CN --> CO[Update PEEQ Value]
        CO --> CP[Continue Next Value]
        CG --> CQ[PEEQ Processing Complete]
        CP --> CQ
    end

    %% Displacement Processing Subgraph
    subgraph DisplacementProcessing[Displacement Processing]
        AK --> CR{Field U Exists}
        CR -->|No| CS[Skip Displacement Processing]
        CR -->|Yes| CT[Extract Displacement Values]
        CT --> CU[Iterate Through Values]
        CU --> CV{Instance Exists}
        CV -->|No| CW[Create Instance Record]
        CV -->|Yes| CX[Retrieve Instance Record]
        CW --> CY[Initialize Displacement Fields]
        CX --> CZ[Process U Component]
        CY --> CZ
        CZ --> DA[Update Magnitude]
        CZ --> DB[Update U1 Component]
        CZ --> DC[Update U2 Component]
        CZ --> DD[Update U3 Component]
        DA --> DE[Continue Next Value]
        DB --> DE
        DC --> DE
        DD --> DE
        CS --> DF[Displacement Processing Complete]
        DE --> DF
    end

    %% Completion and Output Phase
    BA --> DG[Frame Processing Complete]
    BP --> DG
    CE --> DG
    CQ --> DG
    DF --> DG
    
    DG --> DH[End Frame Loop]
    DH --> DI[Check for Next Frame]
    DI --> AE
    
    AC --> DJ[End ODB Processing]
    DJ --> DK[Extract Instance Results]
    DK --> DL[Sort Instances Alphabetically]
    DL --> DM[Iterate Through Instances]
    DM --> DN[Get Record for Instance]
    DN --> DO[Append Row to Results]
    DO --> DP{More Instances}
    DP -->|Yes| DM
    DP -->|No| DQ[Finalize ODB Results]
    DQ --> DR[Close ODB File]
    DR --> DS[Return to File Loop]
    DS --> Q

    %% Final Output Phase
    P --> DT[All Files Processed]
    DT --> DU[Initialize CSV Writer]
    DU --> DV[Write Headers to CSV]
    DV --> DW[Write All Results Rows]
    DW --> DX[Close CSV File]
    DX --> DY[Display Success Message]
    DY --> DZ[Show Output Location]
    DZ --> EA[Script Execution Complete]
    EA --> EB[End]

    %% Apply Styles
    class A,EA,EB startEnd
    class B,C,D,G,I,J,K,L,M,N,O,S,T,U,X,Y,Z,AB,AD,AF,AN,AO,AQ,AR,AS,AT,BD,BE,BG,BH,BI,BJ,BS,BT,BV,BW,BX,BY,CH,CI,CK,CL,CM,CN,CT,CU,CW,CX,CY,CZ,DK,DL,DM,DN,DO,DQ,DR,DT,DU,DV,DW,DX,DY,DZ process
    class E,H,R,V,AA,AE,AL,AP,BB,BF,BQ,BU,CF,CJ,CR,CV,DP decision
    class K,DU,DW io
    class U,AC,DR file
    class F,W error
    class DG,DH,DI,DJ,DS subprocess
    class EA success
    class P,Q loop
