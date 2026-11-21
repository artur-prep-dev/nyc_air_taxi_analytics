[StagingDefinition = [Kind = "FastCopy"]]
section Section1;
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "worldbank_gdp_raw_DataDestination", IsNewTarget = true], Settings = [Kind = "Manual", AllowCreation = true, ColumnSettings = [Mappings = {[SourceColumnName = "indicator_id", DestinationColumnName = "indicator_id"], [SourceColumnName = "indicator_name", DestinationColumnName = "indicator_name"], [SourceColumnName = "country_id", DestinationColumnName = "country_id"], [SourceColumnName = "country_name", DestinationColumnName = "country_name"], [SourceColumnName = "countryiso3code", DestinationColumnName = "countryiso3code"], [SourceColumnName = "date", DestinationColumnName = "date"], [SourceColumnName = "value", DestinationColumnName = "value"], [SourceColumnName = "unit", DestinationColumnName = "unit"], [SourceColumnName = "obs_status", DestinationColumnName = "obs_status"], [SourceColumnName = "decimal", DestinationColumnName = "decimal"]}], DynamicSchema = true, UpdateMethod = [Kind = "Replace"], TypeSettings = [Kind = "Table"]]]}]
shared worldbank_gdp_raw = let
  Source = Json.Document(Web.Contents("https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=100")),
  #"Converted to table" = Table.FromList(Source, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
  Navigation = #"Converted to table"[Column1],
  #"Navigation 1" = Navigation{1},
  #"Converted to table 1" = Table.FromList(#"Navigation 1", Splitter.SplitByNothing(), null, null, ExtraValues.Error),
  #"Expanded Column1" = Table.ExpandRecordColumn(#"Converted to table 1", "Column1", {"indicator", "country", "countryiso3code", "date", "value", "unit", "obs_status", "decimal"}, {"indicator", "country", "countryiso3code", "date", "value", "unit", "obs_status", "decimal"}),
  #"Expanded indicator" = Table.ExpandRecordColumn(#"Expanded Column1", "indicator", {"id", "value"}, {"indicator.id", "indicator.value"}),
  #"Expanded country" = Table.ExpandRecordColumn(#"Expanded indicator", "country", {"id", "value"}, {"country.id", "country.value"}),
  #"Renamed columns" = Table.RenameColumns(#"Expanded country", {{"indicator.id", "indicator_id"}, {"indicator.value", "indicator_name"}, {"country.id", "country_id"}, {"country.value", "country_name"}}),
  #"Changed column type" = Table.TransformColumnTypes(#"Renamed columns", {{"indicator_id", type text}, {"indicator_name", type text}, {"country_id", type text}, {"country_name", type text}, {"countryiso3code", type text}, {"date", Int64.Type}, {"value", type number}, {"unit", type text}, {"obs_status", type text}, {"decimal", Int64.Type}})
in
  #"Changed column type";
shared worldbank_gdp_raw_DataDestination = let
  Pattern = Lakehouse.Contents([HierarchicalNavigation = true, EnableVorder = true, OutputMetadataRefresh = true, CreateNavigationProperties = false, EnableFolding = false]),
  Navigation_1 = Pattern{[workspaceId = "58f3292a-4547-4418-8424-39062a13be44"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "698900e2-825b-490a-9d73-2480fbafe3c5"]}[Data],
  Navigation_3 = Navigation_2{[Id = "dbo", ItemKind = "Schema"]}[Data],
  TableNavigation = Navigation_3{[Id = "worldbank_gdp_raw", ItemKind = "Table"]}?[Data]?
in
  TableNavigation;
