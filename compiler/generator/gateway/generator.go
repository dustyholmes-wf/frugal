/*
 * Copyright 2017 Workiva
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *     http://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package gateway

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/Workiva/frugal/compiler/generator"
	"github.com/Workiva/frugal/compiler/generator/golang"
	"github.com/Workiva/frugal/compiler/parser"
)

const (
	lang                = "gateway"
	defaultOutputDir    = "gen-go" // The gateway depends on the generated Go code, must be placed in same package
	serviceSuffix       = "_service_gateway"
	packagePrefixOption = "package_prefix"
	thriftImportOption  = "thrift_import"
	frugalImportOption  = "frugal_import"
	asyncOption         = "async"
	useVendorOption     = "use_vendor"
)

// Generator implements the LanguageGenerator interface for an HTTP Gateway.
type Generator struct {
	*generator.BaseGenerator
	goGenerator *golang.Generator
	typesFile   *os.File
}

// NewGenerator creates a new gateway LanguageGenerator.
func NewGenerator(options map[string]string) generator.LanguageGenerator {
	return &Generator{
		BaseGenerator: &generator.BaseGenerator{Options: options},
		goGenerator:   &golang.Generator{BaseGenerator: &generator.BaseGenerator{Options: options}, DoGenerateConstants: true, TypesFile: nil},
		typesFile:     nil,
	}
}

//
// Generic methods
//

// SetupGenerator performs any setup logic before generation.
// no-op.
func (g *Generator) SetupGenerator(outputDir string) error {
	g.goGenerator.SetFrugal(g.Frugal)

	return nil
}

// TeardownGenerator cleanups globals the generator needs, like the types file.
func (g *Generator) TeardownGenerator() error {
	return nil
}

// GenerateDependencies generates any dependencies
// no-op.
func (g *Generator) GenerateDependencies(dir string) error {
	return nil
}

// GenerateFile generates the given FileType.
func (g *Generator) GenerateFile(name, outputDir string, fileType generator.FileType) (*os.File, error) {
	switch fileType {
	case generator.CombinedServiceFile:
		return g.CreateFile(strings.ToLower(name)+serviceSuffix, outputDir, "go", true)
	case generator.ServiceArgsResultsFile:
		return g.CreateFile(strings.ToLower(name), outputDir, "go", true)
	default:
		return nil, fmt.Errorf("Bad file type for golang generator: %s", fileType)
	}
}

// GenerateDocStringComment generates the autogenerated notice.
func (g *Generator) GenerateDocStringComment(file *os.File) error {
	return g.goGenerator.GenerateDocStringComment(file)
}

// GenerateConstants generates any static constants.
// no-op
func (g *Generator) GenerateConstants(file *os.File, name string) error {
	return nil
}

// GetOutputDir returns the output directory for generated files.
func (g *Generator) GetOutputDir(dir string) string {
	if namespace := g.Frugal.Namespace(lang); namespace != nil {
		path := generator.GetPackageComponents(namespace.Value)
		dir = filepath.Join(append([]string{dir}, path...)...)
	} else {
		dir = filepath.Join(dir, g.Frugal.Name)
	}
	return dir
}

// DefaultOutputDir returns the default output directory for generated files.
func (g *Generator) DefaultOutputDir() string {
	return defaultOutputDir
}

// PostProcess file runs gofmt and goimports on the given file.
func (g *Generator) PostProcess(f *os.File) error {
	return g.goGenerator.PostProcess(f)
}

//
// Thrift stuff
//

// GenerateTypesImports generates the necessary Go types imports.
func (g *Generator) GenerateTypesImports(file *os.File) error {
	return nil
}

// GenerateConstantsContents generates constants.
// no-op
func (g *Generator) GenerateConstantsContents(constants []*parser.Constant) error {
	return nil
}

// GenerateTypeDef generates the given typedef.
// no-op
func (g *Generator) GenerateTypeDef(typedef *parser.TypeDef) error {
	return nil
}

// GenerateEnum generates the given enum.
// no-op
func (g *Generator) GenerateEnum(enum *parser.Enum) error {
	return nil
}

// GenerateStruct generates the given struct.
// The HTTP proxy creates mappings between JSON annotations and Thrift
func (g *Generator) GenerateStruct(s *parser.Struct) error {
	return nil
}

// GenerateUnion generates the given union.
func (g *Generator) GenerateUnion(union *parser.Struct) error {
	return nil
}

// GenerateException generates the given exception.
func (g *Generator) GenerateException(exception *parser.Struct) error {
	return nil
}

//
// Service-specific methods
//

// GenerateServicePackage generates the package for the given service.
func (g *Generator) GenerateServicePackage(file *os.File, s *parser.Service) error {
	return g.goGenerator.GenerateServicePackage(file, s)
}

// GenerateServiceImports generates necessary imports for the given service.
func (g *Generator) GenerateServiceImports(file *os.File, s *parser.Service) error {
	return g.goGenerator.GenerateServiceImports(file, s)
}

// GenerateService generates the given service.
func (g *Generator) GenerateService(file *os.File, s *parser.Service) error {
	serviceTitle := golang.SnakeToCamel(s.Name)
	contents := ""

	contents += g.generateGatewayContext(serviceTitle)

	for _, method := range s.Methods {

		contents += g.generateHandleFunc(serviceTitle, method)
	}

	contents += g.generateMuxConstructor(s)

	_, err := file.WriteString(contents)
	return err
}

func (g *Generator) generateGatewayContext(serviceTitle string) string {
	var (
		contents    = ""
		contextName = fmt.Sprintf("%sContext", serviceTitle)
	)

	contents += g.GenerateInlineComment([]string{fmt.Sprintf("%s forwards HTTP requests to a Frugal service", contextName)}, "")
	contents += fmt.Sprintf("type %s struct {\n", contextName)
	contents += fmt.Sprintf("\tClient *F%sClient\n", serviceTitle)
	contents += "\tMarshalers gateway.MarshalerRegistry\n"
	contents += "}\n\n"

	contents += g.GenerateInlineComment([]string{fmt.Sprintf("%sHandler is a wrapper to provide context to HTTP handlers", serviceTitle)}, "")
	contents += fmt.Sprintf("type %sHandler struct {\n", serviceTitle)
	contents += fmt.Sprintf("\t*%s\n\n", contextName)

	contents += g.GenerateInlineComment([]string{"ContextHandlerFunc is the interface which our Handlers will implement"}, "")
	contents += fmt.Sprintf("\tContextHandlerFunc func(*%s, http.ResponseWriter, *http.Request) (int, error)\n", contextName)
	contents += "}\n\n"

	contents += g.GenerateInlineComment([]string{"ServeHTTP handles HTTP requests with an included context"}, "")
	contents += fmt.Sprintf("func (handler %sHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {\n", serviceTitle)
	contents += fmt.Sprintf("\tstatus, err := handler.ContextHandlerFunc(handler.%s, w, r)\n", contextName)
	contents += "\tif err != nil {\n"
	contents += "\t\tlog.Printf(\"HTTP %d: %q\", status, err)\n"
	contents += "\t\tswitch status {\n"
	contents += "\t\t\t// TODO:\n"
	contents += "\t\t\t// customize error handling using context\n"
	contents += "\t\t}\n"
	contents += "\t}\n"
	contents += "\n}\n\n"

	return contents
}

func (g *Generator) generateFieldSetter(conversion string, fieldName string) string {
	var contents = ""

	contents += "\t\t\t\t\tc, err := gateway.String(v)\n"
	contents += "\t\t\t\t\tif err != nil {\n"
	contents += "\t\t\t\t\t\tpanic(err)\n"
	contents += "\t\t\t\t\t}\n"

	contents += fmt.Sprintf("\t\t\t\t\tf := s.Field(\"%s\")\n", fieldName)
	contents += "\t\t\t\t\tif strings.Contains(f.Tag(\"json\"), \"omitempty\") {\n"
	contents += "\t\t\t\t\t\terr = f.Set(&c)\n"
	contents += "\t\t\t\t\t} else {\n"
	contents += "\t\t\t\t\t\terr = f.Set(c)\n"
	contents += "\t\t\t\t\t}\n\n"

	return contents
}

func (g *Generator) generateHandleFunc(serviceTitle string, method *parser.Method) string {
	var (
		methodTitle = golang.SnakeToCamel(method.Name)
		contextName = fmt.Sprintf("%sContext", serviceTitle)
		contents    = ""
	)

	// If no HTTP annotation, return without generating handler
	_, found := method.Annotations.Get("http.pathTemplate")
	if !found {
		return ""
	}

	contents += g.GenerateInlineComment([]string{fmt.Sprintf("%s%sHandler forwards HTTP requests to a Frugal service", serviceTitle, methodTitle)}, "")
	contents += fmt.Sprintf("func %s%sHandler(context *%s, responseWriter http.ResponseWriter, request *http.Request) (int, error) {\n", serviceTitle, methodTitle, contextName)

	contents += "\tflusher, _ := responseWriter.(http.Flusher)\n\n"

	contents += "\tinMarshaler, outMarshaler := context.Marshalers.MarshalerForRequest(request)\n\n"

	// Extract the input argument type
	argument := method.Arguments[0]
	contents += g.GenerateInlineComment([]string{"Assemble a Frugal payload of the correct type"}, "\t")
	contents += fmt.Sprintf("\tpayload := &%s{}\n\n", argument.Type.Name)
	contents += "\tdecoder := inMarshaler.NewDecoder(request.Body)\n"
	contents += "\tdefer request.Body.Close()\n"
	contents += "\terr := decoder.Decode(payload)\n"
	contents += "\tif err != nil && err != io.EOF {\n"
	contents += "\t\tpanic(err) // TODO: Customize error handling\n"
	contents += "\t}\n\n"

	contents += g.GenerateInlineComment([]string{"Combine path and query parameters into map[string]string.", "If there are duplicate query parameters, only the first is respected."}, "\t")
	contents += "\tvars := mux.Vars(request)\n"
	contents += "\tqueries := request.URL.Query()\n"
	contents += "\tfor k, v := range queries {\n"
	contents += "\t	vars[k] = v[0]\n"
	contents += "\t}\n\n"

	// Map any path parameters to the payload
	contents += g.GenerateInlineComment([]string{"Map any path or query parameters into the payload"}, "\t")
	parsedStruct := g.Frugal.FindStruct(argument.Type)
	contents += "\ts := gateway.NewStruct(payload)\n"
	contents += "\t\tfor k, v := range vars {\n"
	for _, field := range parsedStruct.Fields {
		fieldName := field.Name
		if jsonProperty, ok := field.Annotations.Get("http.jsonProperty"); ok {
			fieldName = jsonProperty
		}
		contents += fmt.Sprintf("\t\t\t\tif k == \"%s\" {\n", fieldName)
		switch field.Type.String() {
		case "string":
			contents += g.generateFieldSetter(
				"\t\t\t\t\tc, err := gateway.String(v)\n",
				golang.SnakeToCamel(field.Name))
		case "bool":
			contents += g.generateFieldSetter(
				"\t\t\t\t\tc, err := gateway.Bool(v)\n",
				golang.SnakeToCamel(field.Name))
		case "double":
			contents += g.generateFieldSetter(
				"\t\t\t\t\tc, err := gateway.Float64(v)\n",
				golang.SnakeToCamel(field.Name))
		case "i64":
			contents += g.generateFieldSetter(
				"\t\t\t\t\tc, err := gateway.Int64(v)\n",
				golang.SnakeToCamel(field.Name))
		case "i32":
			contents += g.generateFieldSetter(
				"\t\t\t\t\tc, err := gateway.Int32(v)\n",
				golang.SnakeToCamel(field.Name))
		case "i16":
			contents += g.generateFieldSetter(
				"\t\t\t\t\tc, err := gateway.Int16(v)\n",
				golang.SnakeToCamel(field.Name))
		case "i8", "byte":
			contents += g.generateFieldSetter(
				"\t\t\t\t\tc, err := gateway.Int8(v)\n",
				golang.SnakeToCamel(field.Name))
		default:
			contents += fmt.Sprintf("\t\t\t\t\tfmt.Errorf(\"Unsupported conversion of type %s\")\n", field.Type.String())
		}
		contents += "\t\t\t\t}\n"
	}
	contents += "\t\t}\n\n"

	// Pass the payload to the Frugal client
	contents += g.GenerateInlineComment([]string{"Call the Frugal client with the assembled payload"}, "\t")
	contents += fmt.Sprintf("\tresponse, err := context.Client.%s(frugal.NewFContext(\"\"), payload)\n", methodTitle)
	contents += "\tif err != nil {\n"
	contents += "\t\tpanic(err) // TODO: Customize error handling\n"
	contents += "\t}\n\n"

	// Serialize the HTTP response
	contents += g.GenerateInlineComment([]string{"Serialize the Frugal response into a JSON response"}, "\t")
	contents += "\tbuf, err := outMarshaler.Marshal(response)\n"
	contents += "\tif err != nil {\n"
	contents += "\t\tpanic(err) // TODO: Customize error handling\n"
	contents += "\t}\n"

	// Write the response
	contents += "\tresponseWriter.WriteHeader(http.StatusOK)\n"
	contents += "\tresponseWriter.Write(buf)\n"
	contents += "\tflusher.Flush()\n\n"

	contents += "return http.StatusOK, nil\n"
	contents += "}\n\n"

	return contents
}

func (g *Generator) generateMuxConstructor(s *parser.Service) string {
	contents := ""

	contents += g.GenerateInlineComment([]string{"MakeRouter builds a multiplexed router handling HTTP+JSON requests according to IDL annotations"}, "\t")
	contents += "func MakeRouter(context *GatewayTestContext) (*mux.Router, error) {\n"

	// Base router with no handlers
	contents += "\trouter := mux.NewRouter()\n"

	// Add handlers for each service method
	serviceTitle := golang.SnakeToCamel(s.Name)
	for _, method := range s.Methods {
		pathAnnotation, _ := method.Annotations.Get("http.pathTemplate")
		// queryAnnotation, _ := method.Annotations.Get("http.query")  TODO: force query annotations to match
		methodAnnotation, _ := method.Annotations.Get("http.method")

		methodTitle := golang.SnakeToCamel(method.Name)
		interfaceName := fmt.Sprintf("%sHandler", serviceTitle)
		handlerName := fmt.Sprintf("handler%s", methodTitle)
		handlerStructName := fmt.Sprintf("%s%sHandler", serviceTitle, methodTitle)

		contents += fmt.Sprintf("\t%s := &%s{context, %s}\n", handlerName, interfaceName, handlerStructName)
		contents += fmt.Sprintf("\trouter.Methods(\"%s\").Path(\"%s\").Name(\"%s\").Handler(%s)\n", strings.ToUpper(methodAnnotation), pathAnnotation, handlerStructName, handlerName)
	}

	contents += "\t\nreturn router, nil\n"
	contents += "}\n"

	return contents
}

//
// Scope-specific methods
//

// GenerateScopePackage generates the package for the given scope.
func (g *Generator) GenerateScopePackage(*os.File, *parser.Scope) error { return nil }

// GenerateScopeImports generates necessary imports for the given scope.
func (g *Generator) GenerateScopeImports(*os.File, *parser.Scope) error { return nil }

// GeneratePublisher generates the publisher for the given scope.
func (g *Generator) GeneratePublisher(*os.File, *parser.Scope) error { return nil }

// GenerateSubscriber generates the subscriber for the given scope.
func (g *Generator) GenerateSubscriber(*os.File, *parser.Scope) error { return nil }
