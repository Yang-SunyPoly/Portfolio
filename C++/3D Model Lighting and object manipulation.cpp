#include <iostream>
#include <fstream>
#include <sstream>
#include <thread>
#include <vector>
#include <string>
#include <GL/glew.h>					
#include <GLFW/glfw3.h>
#include "glm/glm.hpp"
#include "MeshData.hpp"
#include "MeshGLData.hpp"
#include "GLSetup.hpp"
#include "Shader.hpp"
#include <assimp/Importer.hpp>
#include <assimp/scene.h>
#include <assimp/postprocess.h>
#include "glm/gtc/matrix_transform.hpp"
#define GLM_ENABLE_EXPERIMENTAL
#include "glm/gtx/transform.hpp"
#include "glm/gtx/string_cast.hpp"
#include "glm/gtc/type_ptr.hpp"
#include "Utility.hpp"

using namespace std;

//Global Vars
float themAngles = 0.0f;
glm::vec3 My_Eyes = glm::vec3(0,0,1);
glm::vec3 Cross_Hair = glm::vec3(0,0,0);
glm::vec2 Aim = glm::vec2();
glm::vec4 lightPos(0.5,0.5,0.5,1.0);

glm::mat4 makeLocalRotate(glm::vec3 offset, glm::vec3 axis, float angle)
{
	glm::mat4 You_Spin_Me = glm::translate(offset) * glm::rotate(glm::radians(angle),-axis) * glm::translate(-(offset));
	return You_Spin_Me;
}

static void mouse_position_callback(GLFWwindow* window, double xpos, double ypos)
{
	glm::vec2 RMouse = glm::vec2(xpos - Aim[0],ypos - Aim[1]);

	int fwidth, fheight;
	glfwGetFramebufferSize(window, &fwidth, &fheight);
	if(fwidth > 0 && fheight > 0)
	{
		float WinWF = float(fwidth), WinHF = float(fheight);
		RMouse[0] = RMouse[0] / WinWF;
		RMouse[1] = RMouse[1] / WinHF;
		
		glm::vec4 LocalCrossHair = glm::vec4(Cross_Hair,1.0f);

		LocalCrossHair = makeLocalRotate(My_Eyes,glm::vec3(0.0f,1.0f,0.0f),(30.0f *  RMouse[0])) * makeLocalRotate(My_Eyes,glm::cross((Cross_Hair - My_Eyes),(glm::vec3(0.0f,1.0f,0.0f))),(30.0f * RMouse[1])) * LocalCrossHair;

		Cross_Hair = glm::vec3(LocalCrossHair);
	}

	Aim = glm::vec2(xpos,ypos);

}

glm::mat4 makeRotatz(glm::vec3 offset)
{
	glm::mat4 Thunder_Hammer =  glm::translate(offset) * glm::rotate(glm::radians(themAngles),glm::vec3(0,0,1)) * glm::translate(-(offset));
	
	return Thunder_Hammer;
}

glm::mat4 Ut_Moded(aiNode *node)
{
	glm::mat4 Rebel;
	aiMatToGLM4(node->mTransformation,Rebel);
	return Rebel;
}

void renderScene(vector<MeshGL> &allMeshes, aiNode *node, glm::mat4 parentMat, GLint modelMatLoc, int level,GLint normMatLoc,glm::mat4 viewMat)
{
	glm::mat4 Order_Form_The_Emperor;
	aiMatToGLM4(node->mTransformation,Order_Form_The_Emperor);
	glm::mat4 Cadia_Stands = parentMat * Order_Form_The_Emperor;
	glm::vec3 Terra = glm::vec3(Cadia_Stands[3]); 
	glm::mat4 Warp_Drive = makeRotatz(Terra);

	glm::mat4 Faith_Forever = Warp_Drive * Cadia_Stands;
	glUniformMatrix4fv(modelMatLoc,1, false ,glm::value_ptr(Faith_Forever));

    glm::mat3 Nomral_Mat = glm::transpose(glm::inverse(glm::mat3(viewMat * Faith_Forever)));
    glUniformMatrix3fv(normMatLoc,1,false,glm::value_ptr(Nomral_Mat));


	//glUniformMatrix4fv(modelMatLoc,1, false ,glm::value_ptr((makeRotatz(Ut_Moded(node)[3])) * ((parentMat * Ut_Moded(node))))); //what?

	for (int i = 0; i < node->mNumMeshes; i++)
	{
		int index = node->mMeshes[i];
		drawMesh(allMeshes.at(index));
	}

	for (int i = 0; i < node->mNumChildren ; i++)
	{
		//renderScene(allMeshes, node->mChildren[i], Cadia_Stands, modelMatLoc, level += 1);
		renderScene(allMeshes, node->mChildren[i], (parentMat * Ut_Moded(node)), modelMatLoc, level + 1,normMatLoc,viewMat);
	}

	return;
}

void extractMeshData(aiMesh *mesh, Mesh &m)
{
	m.vertices.clear();
	m.indices.clear();

	for( int i = 0; i < mesh -> mNumVertices; i++)
	{
		Vertex WAAAAH;

		ai_real *x = &mesh -> mVertices[i].x;
		ai_real *y = &mesh -> mVertices[i].y;
		ai_real *z = &mesh -> mVertices[i].z;

        ai_real *N_X = &mesh->mNormals[i].x;
        ai_real *N_Y = &mesh->mNormals[i].y;
        ai_real *N_Z = &mesh->mNormals[i].z;

		WAAAAH.position = glm::vec3(*x,*y,*z);
        WAAAAH.normal = glm::vec3(*N_X,*N_Y,*N_Z);
		WAAAAH.color = glm::vec4(1.0, 1.0, 0.0, 1.0);

		m.vertices.push_back(WAAAAH);
	}

	for (int i = 0; i < mesh->mNumFaces; i ++)
	{
		aiFace Boyz = mesh->mFaces[i];
		
		for (int x = 0; x < Boyz.mNumIndices; x++)
		{
			m.indices.push_back(Boyz.mIndices[x]);
		}
	}
}

static void key_called(GLFWwindow *window, int key, int scancode, int action, int mods)
{
	if(action == GLFW_PRESS || action == GLFW_REPEAT)
	{
		glm::vec3 temp;
		switch (key)
		{
			case GLFW_KEY_ESCAPE:
				glfwSetWindowShouldClose(window, 1);
				break;
			case GLFW_KEY_J:
				themAngles += 1.0f;
				break;
			case GLFW_KEY_K:
				themAngles -= 1.0f;
				break;
			case GLFW_KEY_W:
				temp = glm::normalize(Cross_Hair - My_Eyes) *0.1f;
				My_Eyes += temp;
				Cross_Hair += temp;
				break;
			case GLFW_KEY_S:
				temp = glm::normalize(Cross_Hair - My_Eyes) *0.1f;
				My_Eyes -= temp;
				Cross_Hair -= temp;
				break;
			case GLFW_KEY_A:
				temp = glm::normalize(glm::cross((Cross_Hair - My_Eyes),glm::vec3(0.0f,1.0f,0.0f))) * 0.1f;
				My_Eyes -= temp;
				Cross_Hair -= temp;
				break;
			case GLFW_KEY_D:
				temp = glm::normalize(glm::cross((Cross_Hair - My_Eyes),glm::vec3(0.0f,1.0f,0.0f))) * 0.1f;
				My_Eyes += temp;
				Cross_Hair += temp;
				break;
			default:
				cout << "YO Mr.White, What am I suppose to do with this key?"<<endl;
		}
	}
}

// Main 
int main(int argc, char **argv) {
	
	// Are we in debugging mode?
	bool DEBUG_MODE = true;

	Assimp::Importer Load_it;
	string path = "./sampleModels/sphere.obj";
	if (argc >= 2)
	{
		path = string(argv[1]);
	}
	
	const aiScene *Scriptures = Load_it.ReadFile(path, aiProcess_Triangulate | aiProcess_FlipUVs |aiProcess_GenNormals | aiProcess_JoinIdenticalVertices);	

	if (!Scriptures || Scriptures->mFlags & AI_SCENE_FLAGS_INCOMPLETE || !Scriptures->mRootNode)
	{
		cerr << "Error: " << Load_it.GetErrorString() << endl;
		exit(1);
	}

	// GLFW setup	
	// Switch to 4.1 if necessary for macOS
	GLFWwindow* window = setupGLFW(4, 3, 800, 800, DEBUG_MODE);
	
	double mx,my;
	glfwGetCursorPos(window, &mx, &my);
	Aim = glm::vec2(mx, my);

	glfwSetCursorPosCallback(window,mouse_position_callback);
	glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED); 

	// GLEW setup
	setupGLEW(window);

	// Check OpenGL version
	checkOpenGLVersion();

	// Set up debugging (if requested)
	if(DEBUG_MODE) checkAndSetupOpenGLDebugging();

	// Set the background color to a shade of blue
	glClearColor(0.2f, 0.3f, 0.5f, 1.0f);	 

	glfwSetKeyCallback(window, key_called);

	// Create and load shader
	GLuint programID = 0;
	try {		
		// Load vertex shader code and fragment shader code
		string vertexCode = readFileToString("./shaders/Assign06/Basic.vs");
		string fragCode = readFileToString("./shaders/Assign06/Basic.fs");

		// Print out shader code, just to check
		if(DEBUG_MODE) printShaderCode(vertexCode, fragCode);

		// Create shader program from code
		programID = initShaderProgramFromSource(vertexCode, fragCode);
	}
	catch (exception e) {		
		// Close program
		cleanupGLFW(window);
		exit(EXIT_FAILURE);
	}
	
	vector<MeshGL> GreenSkins;

	for(int i = 0; i < Scriptures->mNumMeshes; i ++)
	{
		Mesh m;
		MeshGL mgl;

		extractMeshData(Scriptures -> mMeshes[i], m);
		createMeshGL(m, mgl);

		GreenSkins.push_back(mgl);
	}

	GLint modMatLoc = glGetUniformLocation(programID,"Something_Something");
	GLint viewMatLoc =  glGetUniformLocation(programID,"Something_View");
	GLint ProjectMatLoc = glGetUniformLocation(programID,"Something_Projection");
    GLint LightMatLoc = glGetUniformLocation(programID,"Something_Light");
    GLint NormalMatLoc = glGetUniformLocation(programID,"Something_Normal");

	// Enable depth testing
	glEnable(GL_DEPTH_TEST);



	while (!glfwWindowShouldClose(window)) {
		// Set viewport size
		int fwidth, fheight;
		glfwGetFramebufferSize(window, &fwidth, &fheight);
		glViewport(0, 0, fwidth, fheight);

		// Clear the framebuffer
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

		// Use shader program
		glUseProgram(programID);
		// Draw object
		//drawMesh(mgl);	

		/*
		for (int i = 0; i < GreenSkins.size(); i++)
		{
			//drawMesh(GreenSkins[i]);
		}
		*/
		glm::mat4 ViewMat = glm::lookAt(My_Eyes,Cross_Hair,glm::vec3(0.0f,1.0f,0.0f));
		glUniformMatrix4fv(viewMatLoc,1,false,glm::value_ptr(ViewMat));
		
        glm::vec4 ViewLight = ViewMat * lightPos;
        glUniform4fv(LightMatLoc,1,glm::value_ptr(ViewLight));

		float ASp = 1.0f;
		
		if(fwidth != 0 && fheight != 0)
		{
			ASp = float(fwidth) / float(fheight);
		}
		
		glm::mat4 ProjectMat = glm::perspective((glm::radians(90.0f)),ASp,0.01f,50.0f);
		glUniformMatrix4fv(ProjectMatLoc,1,false,glm::value_ptr(ProjectMat));
	

		renderScene(GreenSkins, Scriptures->mRootNode, glm::mat4(1.0), modMatLoc,0,NormalMatLoc,ViewMat);

		// Swap buffers and poll for window events		
		glfwSwapBuffers(window);
		glfwPollEvents();

		// Sleep for 15 ms
		this_thread::sleep_for(chrono::milliseconds(15));
	}

	for (int i = 0; i < GreenSkins.size(); i++)
	{
		cleanupMesh(GreenSkins[i]);
	}

	// Clean up shader programs
	glUseProgram(0);
	glDeleteProgram(programID);
		
	// Destroy window and stop GLFW
	cleanupGLFW(window);

	return 0;
}
