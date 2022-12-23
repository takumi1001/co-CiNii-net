
import org.gephi.appearance.api.AppearanceController
import org.gephi.appearance.plugin.RankingNodeSizeTransformer
import org.gephi.filters.api.FilterController
import org.gephi.filters.api.Query
import org.gephi.filters.api.Range
import org.gephi.filters.plugin.graph.DegreeRangeBuilder.DegreeRangeFilter
import org.gephi.graph.api.GraphController
import org.gephi.graph.api.GraphModel
import org.gephi.graph.api.GraphView
import org.gephi.io.exporter.api.ExportController
import org.gephi.io.importer.api.Container
import org.gephi.io.importer.api.EdgeDirectionDefault
import org.gephi.io.importer.api.ImportController
import org.gephi.io.processor.plugin.DefaultProcessor
import org.gephi.preview.api.PreviewController
import org.gephi.preview.api.PreviewProperty
import org.gephi.project.api.ProjectController
import org.gephi.project.api.Workspace
import org.openide.util.Lookup
import java.awt.Font
import java.io.File
import java.io.IOException
import kotlin.system.exitProcess


fun main(args: Array<String>) {

    initAndLoadGraph(args[0])

    val graphModel = Lookup.getDefault().lookup(GraphController::class.java).graphModel
    val graph = graphModel.undirectedGraph
    println("Graph loaded successfully: ${args[0]}")
    println("\tNodes: " + graph.nodeCount)
    println("\tEdges: " + graph.edgeCount)

    val appearanceController = Lookup.getDefault().lookup(
        AppearanceController::class.java
    )

    rankSizeByDegree(graphModel, appearanceController)
    hideOneDegreeNodes(graphModel)

    //Gephi Toolkitのバグにより、PDFにすると日本語が出力できない・・・。
    previewGraph("メイリオ")
    exportFile("output.svg")
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