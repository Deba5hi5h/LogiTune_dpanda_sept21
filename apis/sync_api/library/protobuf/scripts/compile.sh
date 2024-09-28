#!/bin/bash

PROTO_HOME=`dirname "$(stat -f "$0")"`
PROTO_HOME=$PROTO_HOME/..

outputDir=$PROTO_HOME

print_usage() {
	echo 
	echo "OVERVIEW: Compiles the selected Protocol Buffer modules to the language of"
	echo "your choice. The compiled files are placed into the root directory of this"
	echo "project by default if no output path is specified."
	echo
	echo "USAGE: compile.sh [-m <module_name>] [-l <language_name>] <output_path>"
	echo
	echo "OPTIONS:"
	echo "  -m <module_name>  The name of the module to include during compilation."
	echo "                    Multiple modules can be specified by using this option"
	echo "                    multiple times. At least one module must be specified."
	echo "                    See the list of valid modules at the end of this usage"
	echo "                    guide."
	echo " -l <language_name> The language to compile the Protocol Buffer messages to."
	echo "                    Multiple languages can be specified by using this option"
	echo "                    multiple times. At least one language must be specified."
	echo "                    See the list of valid languages at the end of this usage"
	echo "                    guide."
	echo
	echo "MODULES:"
	echo "  sync   - Public Protocol Buffer message definitions for the Sync"
	echo "           ecosystem."
	echo "  raiden - Private Protocol Buffer message definitions for cloud-specific"
	echo "           tasks. Dependent on the sync module so that module must be"
	echo "           included when building this module."
	echo
	echo "EXAMPLES:"
	echo "  # Compiles the sync module messages to C++."
	echo "  compile.sh -m sync -l cpp"
	echo
	echo "  # Compiles the sync and raiden modules to C++, Java, and Python."
	echo "  compile.sh -m sync -m raiden -l cpp -l java -l python"
	echo 
}

while getopts ":m:hl:" option
do
	case "$option" in
		h) 
			print_usage
			exit 0
			;;
		m) 
			modules+=("$OPTARG")
			;;
		l)
			languages+=("$OPTARG")
			;;
		*) break
			echo "ERROR: Invalid option given ( $option )."
			print_usage
			exit 1
			;;
	esac
done

shift $(($OPTIND - 1))

if [ ! -z "$1" ] ; then
	outputDir=$1
fi

if [ ${#modules[@]} -eq 0 ] || [ ${#languages[@]} -eq 0 ] ; then
	echo "ERROR: At least one module and language must be specified."
	print_usage
	exit 1
fi

compiledDir="$outputDir/compiled"

for module in "${modules[@]}"
do
	protoPath="$protoPath -I $PROTO_HOME/$module"
	inputPath="$inputPath $PROTO_HOME/$module/*.proto"
done

options=""

for language in "${languages[@]}"
do
	case "$language" in
	"cpp")
		langOutDir="$compiledDir/cpp"
		langOutCmd="--cpp_out=$langOutDir"
	    ;;
	"java")
		langOutDir="$compiledDir/java"
	    langOutCmd="--java_out=$langOutDir"
	    ;;
	"python")
		langOutDir="$compiledDir/python"
		langOutCmd="--python_out=$langOutDir"
		;;
	"csharp")
		langOutDir="$compiledDir/csharp"
		langOutCmd="--csharp_out=$langOutDir"
		;;
	"js")
		langOutDir="$compiledDir/js"
		langOutCmd="--js_out=import_style=commonjs,binary:$langOutDir"
		;;
	*)
		echo "ERROR: Unknown language ( $language ). See list of supported languages."
		echo
		print_usage
		exit 1
	    ;;
	esac

	languageSpecifier="${languageSpecifier} ${langOutCmd}"

	rm -rf "$langOutDir/*"
	if [ ! -d "$langOutDir" ] ; then
		mkdir -p "$langOutDir"
	fi
done

echo
echo "Executing 'protoc $protoPath $languageSpecifier $inputPath'"

protoc $protoPath $languageSpecifier $inputPath

echo "  ...Compiled files generated in ${compiledDir}!"
echo
