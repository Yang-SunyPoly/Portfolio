#include "PotatoForwardEngine.hpp" 
 
PotatoForwardEngine::PotatoForwardEngine(int windowWidth, int windowHeight) : PotatoRenderEngine(windowWidth, windowHeight) { 
    // For now, generate simple fan 
    PolyMesh* Adding = loadOBJModel("./sampleModels/teapot.obj");
    PolyMesh* Addingg = loadOBJModel("./sampleModels/sphere.obj");
    vector<Vert> Copy_Vert = Addingg->getVertices();
    int size_of_Vert = Copy_Vert.size(); // siz
        for (int i = 0; i < size_of_Vert; i++)
        {
            Addingg->getVertices().at(i).pos =  Addingg->getVertices().at(i).pos - PUSH;
        }
    allMeshes.push_back(Adding);
    allMeshes.push_back(Addingg);
    PolyMesh* Copy = new PolyMesh(Adding); // this works?
    PolyMesh* Copyy = new PolyMesh(Addingg); 
    renderMeshes.push_back(Copy);
    renderMeshes.push_back(Copyy);

    //for(int i = 0; i < MAX_THREAD_CNT; i++) {
    //    allThreads.push_back(new thread(&PotatoForwardEngine::threadWorkerFunc, this));
    //}
} 

void PotatoForwardEngine::threadWorkerFunc() {
    while(stillWorking) {
        
        if(rowsToDo.size() > 0) {
            rowListLock.lock();
            if(rowsToDo.size() > 0) {
                int row = rowsToDo[rowsToDo.size()-1];
                rowsToDo.pop_back();
                cout << "Thread working on " << row << endl;
            }
            rowListLock.unlock();
        }
        else {
            this_thread::sleep_for(chrono::milliseconds(50));
        }        
    }
}


Mat4f PotatoForwardEngine::Camera(Vec3i Location, Vec3f Look){
    Vec3f Off, U, V,  W;
    Off = Look - Location;
    Off = Off.normalize();

    W = Off * -1;
    U = Off.cross(Vec3f(0.0f, 1.0f, 0.0f)).normalize();
    V = W.cross(U).normalize();

    return (U, 0.0f, V, 0.0f, W, 0.0f, 0.0f, 0.0f, 0.0f, 1.0f);
}

void PotatoForwardEngine::Light(vector<Fragment> &fragList)
{
    for(int i = 0; i < fragList.size(); i++) { 
        fragList.at(i).color = B_Phong(fragList.at(i));
    }
}

Vec4f PotatoForwardEngine::B_Phong(Fragment Frag){
            
        Vec3f Fragpos = Vec3f(Frag.viewPos);
        Vec3f Fragcolor = Vec3f(Frag.color);
        Vec3f Fragnormal = Vec3f(Frag.normal).normalize();

        Vec3f L = (LIGHTPOS - Fragpos);
        L = L.normalize();
        Vec3f V = (CAMPOS - Fragpos);
        V = V.normalize();
        Vec3f H = (V+L).normalize();

        Vec4f First;
        First = Vec4f(Fragcolor*max(0.0f, Fragnormal.dot(L)), 1.0f);
        Vec4f Secound;
        Secound = Vec4f(255.0f,255.0f,255.0f,1.0f);

        Vec3f Shin;
        Shin = Shin * max(0.0f, Fragnormal.dot(H));
        for (int i = 0; i < SHININESS; i++)
        {
            Shin = Shin * max(0.0f, Fragnormal.dot(H));
        }

        Secound = Secound * Vec4f(Fragcolor*max(0.0f, Fragnormal.dot(L)) * Shin , 1.0f);
        First = First + Secound;
    
        return First;
}

 
PotatoForwardEngine::~PotatoForwardEngine() { 
    stillWorking = false;
    for(int i = 0; i < allThreads.size(); i++) {
        allThreads[i]->join();
        delete allThreads[i];
    }
    allThreads.clear();

    // Clean up meshes 
    for(int i = 0; i < allMeshes.size(); i++) { 
        delete allMeshes.at(i); 
    } 
    allMeshes.clear(); 
 
    //allFragments.clear(); 

    for(int i = 0; i < renderMeshes.size(); i++) { 
        delete renderMeshes.at(i); 
    } 
    renderMeshes.clear(); 
 
    allFragments.clear(); 
} 
 
void PotatoForwardEngine::processGeometryOneMesh(PolyMesh* inputMesh, Mat4f& modelMat, Mat4f& viewMat, Mat4f& projMat, PolyMesh* outMesh){ //Am I not suppose add PotatoForwardEngine::
    vector<int> Clip_Code;
    vector<Vert> Copy_Vert = inputMesh->getVertices();
    int size_of_Vert = Copy_Vert.size(); // siz
    for (int i = 0; i < size_of_Vert; i++)
    {
        Vec4f NewV4 = {Copy_Vert.at(i).pos, 1.0f};
        Vec4f NewV4_X = {0.0f,0.0f,0.0f,1.0f};

        NewV4 = projMat * viewMat * modelMat * NewV4;
        //NewV4_X  = viewMat * modelMat * {Copy_Vert.at(i).pos, 1.0f};

        outMesh -> getVertices().at(i).depth = NewV4.z;

        Clip_Code.push_back(getExtendedCohenSutherlandCode(NewV4, CLIP_LEFT, CLIP_RIGHT, CLIP_BOTTOM, CLIP_TOP, CLIP_NEAR, CLIP_FAR));
        NewV4[0] = NewV4[0]/NewV4[3];
        NewV4[1] = NewV4[1]/NewV4[3];
        NewV4[2] = NewV4[2]/NewV4[3];

        outMesh->getVertices().at(i).pos = {NewV4[0], NewV4[1], NewV4[2]}; //ummm I dk what I am doing anymore
    }
        outMesh->getFaces().clear();
        vector <Face> Copy_Face = inputMesh->getFaces();
        int size_of_face = Copy_Face.size();
        for (int i = 0; i < size_of_face; i++)
        {
            int Code0 = Clip_Code[Copy_Face[i].indices[0]];
            int Code1 = Clip_Code[Copy_Face[i].indices[1]];
            int Code2 = Clip_Code[Copy_Face[i].indices[2]];

            if ( Code0 == 0 && Code1 == 0 && Code2 == 0)
            {
                outMesh->getFaces().push_back(inputMesh->getFaces().at(i));
            }
        }

        vector<Vert> Copy_Vert_Out = outMesh->getVertices();
        int size_of_out_vert = Copy_Vert_Out.size();


        for (int i = 0; i < size_of_out_vert; i++)
        {
            Vec3f pos = outMesh->getVertices().at(i).pos;
            outMesh->getVertices().at(i).pos[0] = windowWidth * (pos[0] + 1.0f)/2.0f;
            outMesh->getVertices().at(i).pos[1] = windowHeight * (pos[1] + 1.0f)/2.0f;
            //outMesh->getVertices().at(i).pos = pos;
        }
    }


void PotatoForwardEngine::mergeFragments(vector<Fragment> &fragList, Image<Vec3f> *drawBuffer) { 
    // For now, just blindly write all fragments to buffer 
    for(int i = 0; i < fragList.size(); i++) { 
        Fragment f = fragList.at(i);
        if (f.depth > ZBuffer->getPixel(f.pos.x, f.pos.y))
        {
            ZBuffer->setPixel(f.pos.x, f.pos.y, f.depth);
            drawBuffer->setPixel(f.pos.x, f.pos.y, Vec3f(f.color));
        }
    } 
} 
 
void PotatoForwardEngine::renderToDrawBuffer(Image<Vec3f> *drawBuffer) { 
 
    ZBuffer->clear(-99.0f);

    // Clear list of fragments 
    allFragments.clear(); 
 
    for(int i = 0; i < allMeshes.size(); i++) { 
        //PolyMesh *mesh = allMeshes.at(i); 
        PolyMesh *In = allMeshes.at(i);
        PolyMesh *mesh = renderMeshes.at(i);
        Mat4f Cam = Camera(CAMPOS, CAMLOOK);
 
        processGeometryOneMesh(In, Mat4f(1.0f), Cam, Mat4f(1.0f),mesh);//Mat4f(1.0f),Mat4f(1.0f)
        // Get fragments for inside of polygons 
         fillTriangles(mesh, allFragments);  // Change this for ScreenSHot
 
        // Get fragments for lines 
        drawLines(mesh, allFragments, DRAW_LINES_AS_WIREFRAME); 
    } 
 
    Light(allFragments);
    // Merge fragments 
    mergeFragments(allFragments, drawBuffer); 

    while(rowsToDo.size() != 0) {
        this_thread::sleep_for(chrono::milliseconds(20));
    }
} 
 
