import org.gephi.appearance.api.AppearanceController
import org.gephi.appearance.api.PartitionFunction
import org.gephi.appearance.plugin.PartitionElementColorTransformer
import org.gephi.appearance.plugin.RankingNodeSizeTransformer
import org.gephi.appearance.plugin.palette.Palette
import org.gephi.appearance.plugin.palette.PaletteManager
import org.gephi.appearance.plugin.palette.Preset
import org.gephi.filters.api.FilterController
import org.gephi.filters.api.Query
import org.gephi.filters.api.Range
import org.gephi.filters.plugin.graph.DegreeRangeBuilder.DegreeRangeFilter
import org.gephi.graph.api.*
import org.gephi.io.exporter.api.ExportController
import org.gephi.io.importer.api.Container
import org.gephi.io.importer.api.EdgeDirectionDefault
import org.gephi.io.importer.api.ImportController
import org.gephi.io.processor.plugin.DefaultProcessor
import org.gephi.layout.plugin.noverlap.NoverlapLayout
import org.gephi.layout.plugin.noverlap.NoverlapLayoutBuilder
import org.gephi.layout.plugin.openord.OpenOrdLayout
import org.gephi.layout.plugin.openord.OpenOrdLayoutBuilder
import org.gephi.preview.api.PreviewController
import org.gephi.preview.api.PreviewProperty
import org.gephi.project.api.ProjectController
import org.gephi.project.api.Workspace
import org.openide.util.Lookup
import java.awt.Color
import java.awt.Font
import java.io.File
import java.io.IOException
import kotlin.system.exitProcess

fun main(args: Array<String>) {
    var fontName = "IPA Gothic"
    if(args.size < 2) {
        println("Usage:")
        println("\tjava -jar ./visualizer.jar input.graphml output.svg [font name]")
        println("Args:")
        println("\tinput.graphml \t... co-CiNii-net's GraphML file.")
        println("\t output.svg \t... Output file name and ext. (.svg, .png, .pdf and more allowed.)")
        println("\t [font name] \t... [Optional] Specify label font. Default is `IPA Gothic`.")
        println("\n　* Exporting PDF function has problems in printing multi-byte characters.")
        println("　* Specified font is ignored when it not found.")
        return
    }else if(args.size == 3) {
        fontName = args[2]
    }else if(args.size > 3) {
        println("Too many args!!")
        println("When no args provided, you can see usage.")
        return
    }

    initAndLoadGraph(args[0])

    val graphModel = Lookup.getDefault().lookup(GraphController::class.java).graphModel
    val graph = graphModel.undirectedGraph
    println("Graph loaded successfully: ${args[0]}")

    val appearanceController = Lookup.getDefault().lookup(
        AppearanceController::class.java
    )

    println("OpenOrdLayout: Start")
    layoutByOpenOrd(graphModel)
    println("OpenOrdLayout: Done")
    rankSizeByDegree(graphModel, appearanceController)
    hideOneDegreeNodes(graphModel)
    layoutByNoverlap(graphModel)
    try {
        coloredByCluster(graphModel, appearanceController)
    }catch (ex :Exception) {
        println("This graph doesn't have `cluster` columns.")
        for (node in graphModel.graph.nodes) {
            node.color = Color(0xA8B1FF) //クリアな青色
        }
    }

    //Gephi Toolkitのバグにより、PDFにすると日本語が出力できない・・・。
    previewGraph(fontName)
    exportFile(args[1])

    println("Graph exported successfully: ${args[1]}")
}

fun initAndLoadGraph(inputPath :String) {
    val pc: ProjectController = Lookup.getDefault().lookup(ProjectController::class.java)
    pc.newProject()
    val workspace: Workspace = pc.currentWorkspace

    val importController = Lookup.getDefault().lookup(
        ImportController::class.java
    )

    val container: Container
    try {
        val file = File(inputPath)
        container = importController.importFile(file)
        container.loader.setEdgeDefault(EdgeDirectionDefault.UNDIRECTED) //Force UNDIRECTED
        importController.process(container, DefaultProcessor(), workspace)
    } catch (ex: Exception) {
        ex.printStackTrace()
        println("Failed loading a graph file: $inputPath")
        exitProcess(1)
    }
}

fun exportFile(outputPath :String) {
    val ec = Lookup.getDefault().lookup(ExportController::class.java)
    try {
        ec.exportFile(File(outputPath))
    } catch (ex: IOException) {
        ex.printStackTrace()
        println("Failed exporting: $outputPath")
        exitProcess(1)
    }
}

fun rankSizeByDegree(graphModel: GraphModel, appearanceController: AppearanceController) {
    val appearanceModel = appearanceController.model

    val degreeRanking = appearanceModel.getNodeFunction(
        graphModel.defaultColumns().degree(),
        RankingNodeSizeTransformer::class.java
    )
    val degreeTransformer: RankingNodeSizeTransformer = degreeRanking.getTransformer()
    degreeTransformer.minSize = 10f
    degreeTransformer.maxSize = 72f
    appearanceController.transform(degreeRanking)
}

fun coloredByCluster(graphModel: GraphModel, appearanceController: AppearanceController) {
    //GraphMLは属性の仕組みがやや複雑で、変な処理が必要
    var colId = "cluster"
    for (col in graphModel.nodeTable){
        if (col.title == "cluster") {
            colId = col.id
        }
    }
    val clusterColumn: Column = graphModel.nodeTable.getColumn(colId)  //throw exception if non-clustered

    val clusterCount = getClusterCount(graphModel.graph, clusterColumn)
    val intensePreset = Preset(
        "Intense",
        false,
        0,
        360,
        0.6f,
        3f,
        0.2f,
        1.1f
    )   // cf.https://github.com/gephi/gephi/blob/master/modules/AppearancePlugin/src/main/resources/org/gephi/appearance/plugin/palette/palette_presets.csv
    val palette: Palette = PaletteManager.getInstance().generatePalette(clusterCount, intensePreset)

    val appearanceModel = appearanceController.model
    val clusterPartitionFunction = appearanceModel.getNodeFunction(
        clusterColumn,
        PartitionElementColorTransformer::class.java
    )
    val clusterPartition = (clusterPartitionFunction as PartitionFunction).partition
    clusterPartition.setColors(graphModel.graph, palette.colors);
    appearanceController.transform(clusterPartitionFunction)
}

fun getClusterCount(graph: Graph, clusterColumn: Column): Int {
    var maxId = 0
    for(node in graph.nodes) {
        val clusterId = node.getAttribute(clusterColumn) as Long
        if(maxId < clusterId) {
            maxId = clusterId.toInt()
        }
    }
    return maxId
}

fun hideOneDegreeNodes(graphModel :GraphModel) {
    val graph = graphModel.undirectedGraph

    val filterController = Lookup.getDefault().lookup(
        FilterController::class.java
    )

    val degreeFilter = DegreeRangeFilter()
    degreeFilter.init(graph)
    degreeFilter.range = Range(2, Int.MAX_VALUE) //Remove degree=1

    val query: Query = filterController.createQuery(degreeFilter)
    val view: GraphView = filterController.filter(query)
    graphModel.visibleView = view
}

fun previewGraph(fontName :String) {
    val model = Lookup.getDefault().lookup(PreviewController::class.java).model
    model.properties.putValue(PreviewProperty.SHOW_NODE_LABELS,true)
    val font = Font(fontName, Font.PLAIN, 8)
    model.properties.putValue(
        PreviewProperty.NODE_LABEL_FONT,
        font)
}

fun layoutByOpenOrd(graphModel: GraphModel) {
    val layout = OpenOrdLayout(OpenOrdLayoutBuilder())
    layout.setGraphModel(graphModel)
    layout.resetPropertiesValues()
    layout.initAlgo()
    for(i in 1..layout.numIterations) {
        layout.goAlgo()
        if (!layout.canAlgo()) break
    }
    layout.endAlgo()
}

fun layoutByNoverlap(graphModel: GraphModel) {
    val layout = NoverlapLayout(NoverlapLayoutBuilder())
    layout.setGraphModel(graphModel)
    layout.resetPropertiesValues()
    layout.initAlgo()
    while (layout.canAlgo()) {
        layout.goAlgo()
    }
    layout.endAlgo()
}
