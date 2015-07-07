/* build command
g++ main.cpp -std=gnu++11 -lGL -lglut -LGLES3 -o main
*/

#include <cstdint>
#include <iostream>
#include <vector>
using namespace std;
#include "GL/freeglut.h"
#include <GLES3/gl3.h>

GLuint p;

char* read_file(const char* fn) {
    FILE *fp;
    char* content = NULL;
    int count=0;

    if (fn != NULL) {
        fp = fopen(fn,"rt");

        if (fp != NULL) {
            fseek(fp, 0, SEEK_END);
            count = ftell(fp);
            rewind(fp);

            if (count > 0) {
                content = (char* )malloc(sizeof(char) * (count+1));
                count = fread(content,sizeof(char),count,fp);
                content[count] = '\0';
            }
            fclose(fp);
        }
    }
    return content;
}

void check_shader(GLuint shader) {
    GLint success;
    glGetShaderiv(shader, GL_COMPILE_STATUS, &success);
    if (success != GL_TRUE)
        exit(1);
}


GLuint load_shader(const char *shader_name, GLenum type) {
    GLuint shader = glCreateShader(type);
    char *shader_source = read_file(shader_name);
    glShaderSource(shader, 1, &shader_source, NULL);
    free(shader_source);
    glCompileShader(shader);
    check_shader(shader);
    return shader;
}

void renderFunction() {
    glClearColor(0.0, 0.0, 0.0, 0.0);
    glClear(GL_COLOR_BUFFER_BIT);

    glUseProgram(p);

    // logic begin
    GLint world23 = glGetUniformLocation(p, "world23");
    GLint world24 = glGetUniformLocation(p, "world24");
    GLint world32 = glGetUniformLocation(p, "world32");
    GLint world34 = glGetUniformLocation(p, "world34");
    GLint world4 = glGetUniformLocation(p, "world4");
    GLint world42 = glGetUniformLocation(p, "world42");
    GLint world43 = glGetUniformLocation(p, "world43");

    cout << world23 << endl
         << world24 << endl
         << world32 << endl
         << world34 << endl
         << world4 << endl
         << world42 << endl
         << world43 << endl;

    vector<uint8_t>* zero_buffer = new vector<uint8_t>();
    uint32_t size = sizeof(GLfloat) * 16;
    zero_buffer->resize(size);
    void* zero = &(*zero_buffer)[0];
    cout << glGetError() << endl;

    glUniformMatrix4fv(world4, 1, false, reinterpret_cast<const GLfloat*>(zero));
    cout << glGetError() << endl;

    glUniformMatrix2x3fv(world23, 1, false, reinterpret_cast<const GLfloat*>(zero));
    cout << glGetError() << endl;
    glUniformMatrix3x2fv(world32, 1, false, reinterpret_cast<const GLfloat*>(zero));
    cout << glGetError() << endl;

    glUniformMatrix4x2fv(world42, 1, false, reinterpret_cast<const GLfloat*>(zero));
    cout << glGetError() << endl;
    glUniformMatrix4x3fv(world43, 1, false, reinterpret_cast<const GLfloat*>(zero));
    cout << glGetError() << endl;

    // logic end

    glutSwapBuffers();
}

int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitContextVersion(3, 0);
    glutInitDisplayMode(GLUT_SINGLE);
    glutInitWindowSize(500, 500);
    glutInitWindowPosition(100, 100);
    glutCreateWindow("OpenGL Example");

    p = glCreateProgram();

    GLuint vshader = load_shader("shader1.vert", GL_VERTEX_SHADER);
    GLuint fshader = load_shader("shader1.frag", GL_FRAGMENT_SHADER);

    glAttachShader(p, vshader);
    glAttachShader(p, fshader);

    glLinkProgram(p);
    glutDisplayFunc(renderFunction);
    glutMainLoop();
    return 0;
}
