from django.contrib import admin

from .models import AllowedConnection, BlockType, PortDefinition


class PortDefinitionInline(admin.TabularInline):
    model = PortDefinition
    extra = 1
    fields = (
        "code",
        "name",
        "label",
        "direction",
        "data_type",
        "required",
        "multiple",
        "order",
        "is_active",
    )
    ordering = ("direction", "order")
    show_change_link = True


@admin.register(BlockType)
class BlockTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "extension",
        "default_method",
        "is_active",
        "order",
        "port_count",
    )
    list_filter = ("extension", "is_active")
    search_fields = ("name", "code", "description")
    ordering = ("order", "name")
    prepopulated_fields = {"code": ("name",)}
    inlines = [PortDefinitionInline]

    @admin.display(description="Ports")
    def port_count(self, obj: BlockType) -> int:
        return obj.ports.count()


@admin.register(PortDefinition)
class PortDefinitionAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "block_type",
        "direction",
        "data_type",
        "required",
        "multiple_display",
        "is_active",
        "order",
    )
    list_filter = ("direction", "data_type", "required", "multiple", "is_active", "block_type")
    search_fields = ("code", "name", "label", "block_type__code", "block_type__name")
    ordering = ("block_type", "direction", "order")
    list_editable = ("required", "is_active", "order")
    raw_id_fields = ("block_type",)

    @admin.display(description="Relation", boolean=False)
    def multiple_display(self, obj: PortDefinition) -> str:
        return "many" if obj.multiple else "1:1"

    fieldsets = (
        (None, {
            "fields": ("block_type", "code", "name", "label", "direction", "data_type"),
        }),
        ("Connection behaviour", {
            "fields": ("required", "multiple"),
            "description": (
                "multiple=False → port accepts only one connection (1:1). "
                "multiple=True → port accepts many incoming/outgoing connections."
            ),
        }),
        ("Meta", {
            "fields": ("order", "is_active"),
        }),
    )


@admin.register(AllowedConnection)
class AllowedConnectionAdmin(admin.ModelAdmin):
    list_display = (
        "source_port",
        "target_port",
        "require_same_extension",
        "is_active",
        "note",
    )
    list_filter = ("require_same_extension", "is_active")
    search_fields = (
        "source_port__code",
        "target_port__code",
        "source_port__block_type__code",
        "target_port__block_type__code",
        "note",
    )
    raw_id_fields = ("source_port", "target_port")
    list_editable = ("is_active",)
